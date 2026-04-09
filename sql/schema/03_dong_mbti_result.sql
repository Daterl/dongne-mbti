-- ============================================================
-- 03. DONG_MBTI_RESULT — 동별 MBTI 판정 테이블
-- v4: DataKnows 피처 통합 (#21)
--   S/N 축 ← 역세권 거리 추가 (avg_subway_distance_m)
--   T/F 축 ← DataKnows AI 시세 교체 (dk_avg_price_pyeong)
--   J/P 축 ← DataKnows AI 변동성 우선 (dk_price_cv → price_cv 폴백)
-- z-score 정규화 → 4축 점수 → MBTI 4글자 판정
-- 의존: DONG_FEAT_EI, DONG_FEAT_SN, DONG_FEAT_TF, DONG_FEAT_JP,
--       DONG_FEAT_SUBWAY, DONG_FEAT_DK_PRICE
-- 크레딧: ~$0.01 (~118건 연산)
-- ============================================================
-- ⚠️ S/N 축 피처 4개 (이전 3개):
--   practical_ratio(+S), edu_ratio(+S), culture_ratio(-S), avg_subway_distance_m(+S)
-- ⚠️ T/F 축: avg_price → dk_avg_price_pyeong (DataKnows AI 시세)
-- ⚠️ J/P 축: price_cv → COALESCE(dk_price_cv, price_cv) (DataKnows 우선)
-- ============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;

CREATE OR REPLACE TABLE DONG_MBTI_RESULT AS
WITH
-- 6개 피처 테이블 합치기
features AS (
    SELECT
        ei.SGG,
        ei.EMD,
        ei.CITY_CODE,
        ei.DISTRICT_CODE,
        -- E/I 피처 (SPH 유동인구 + 카드소비)
        ei.visit_ratio,
        ei.weekend_ratio,
        ei.ent_ratio,
        -- S/N 피처 (SPH 카드소비 + DataKnows 역세권)
        sn.practical_ratio,
        sn.edu_ratio,
        sn.culture_ratio,                     -- ⚠️ N 방향: 부호 반전 필요
        sb.avg_subway_distance_m,             -- ⚠️ S 방향 (+): 거리 클수록 S(주거/실용)
        -- T/F 피처 (SPH 자산 + DataKnows AI 시세)
        tf.avg_income,
        tf.avg_asset,
        COALESCE(dk.dk_avg_price_pyeong,
                 tf.avg_price)               AS tf_price,   -- DataKnows 우선, RICHGO 폴백
        -- J/P 피처 (DataKnows AI 변동성 우선 + RICHGO 폴백 + 인구구조)
        COALESCE(dk.dk_price_cv,
                 jp.price_cv)               AS jp_price_cv, -- DataKnows 우선, RICHGO 폴백
        jp.young_ratio
    FROM DONG_FEAT_EI ei
    JOIN DONG_FEAT_SN sn ON ei.DISTRICT_CODE = sn.DISTRICT_CODE
    JOIN DONG_FEAT_TF tf ON ei.DISTRICT_CODE = tf.DISTRICT_CODE
    JOIN DONG_FEAT_JP jp ON ei.DISTRICT_CODE = jp.DISTRICT_CODE
    LEFT JOIN DONG_FEAT_SUBWAY sb ON ei.DISTRICT_CODE = sb.DISTRICT_CODE
    LEFT JOIN DONG_FEAT_DK_PRICE dk ON ei.DISTRICT_CODE = dk.DISTRICT_CODE
),

-- z-score 정규화용 통계
stats AS (
    SELECT
        -- E/I
        AVG(visit_ratio) AS m_vr, STDDEV(visit_ratio) AS s_vr,
        AVG(weekend_ratio) AS m_wr, STDDEV(weekend_ratio) AS s_wr,
        AVG(ent_ratio) AS m_er, STDDEV(ent_ratio) AS s_er,
        -- S/N (4개)
        AVG(practical_ratio) AS m_pr, STDDEV(practical_ratio) AS s_pr,
        AVG(edu_ratio) AS m_edr, STDDEV(edu_ratio) AS s_edr,
        AVG(culture_ratio) AS m_cr, STDDEV(culture_ratio) AS s_cr,
        AVG(avg_subway_distance_m) AS m_sd, STDDEV(avg_subway_distance_m) AS s_sd,
        -- T/F
        AVG(avg_income) AS m_ai, STDDEV(avg_income) AS s_ai,
        AVG(avg_asset) AS m_aa, STDDEV(avg_asset) AS s_aa,
        AVG(tf_price) AS m_tp, STDDEV(tf_price) AS s_tp,
        -- J/P
        AVG(jp_price_cv) AS m_pcv, STDDEV(jp_price_cv) AS s_pcv,
        AVG(young_ratio) AS m_yr, STDDEV(young_ratio) AS s_yr
    FROM features
),

-- z-score 적용 + 축별 점수 계산
scored AS (
    SELECT
        f.SGG,
        f.EMD,
        f.CITY_CODE,
        f.DISTRICT_CODE,

        -- E/I 점수: 양수 = E(외향/활동), 음수 = I(내향/조용)
        ROUND((
            (f.visit_ratio - s.m_vr)   / NULLIF(s.s_vr, 0) +
            (f.weekend_ratio - s.m_wr) / NULLIF(s.s_wr, 0) +
            (f.ent_ratio - s.m_er)     / NULLIF(s.s_er, 0)
        ) / 3, 4) AS ei_score,

        -- S/N 점수: 양수 = S(실용/주거), 음수 = N(문화/도시)
        -- practical_ratio(+S), edu_ratio(+S) → S 방향
        -- culture_ratio(-S) → N 방향 (부호 반전)
        -- avg_subway_distance_m(+S) → 역 멀수록 S(주거지), 가까울수록 N(도시적)
        ROUND((
            (f.practical_ratio - s.m_pr)               / NULLIF(s.s_pr, 0)  +
            (f.edu_ratio - s.m_edr)                    / NULLIF(s.s_edr, 0) -
            (f.culture_ratio - s.m_cr)                 / NULLIF(s.s_cr, 0)  +
            (f.avg_subway_distance_m - s.m_sd)         / NULLIF(s.s_sd, 0)
        ) / 4, 4) AS sn_score,

        -- T/F 점수: 양수 = T(경제/부유), 음수 = F(서민/생활)
        -- DataKnows AI 시세 사용 (기존 RICHGO avg_price 대체)
        ROUND((
            (f.avg_income - s.m_ai) / NULLIF(s.s_ai, 0) +
            (f.avg_asset - s.m_aa)  / NULLIF(s.s_aa, 0) +
            (f.tf_price - s.m_tp)   / NULLIF(s.s_tp, 0)
        ) / 3, 4) AS tf_score,

        -- J/P 점수: 양수 = P(변화/유동), 음수 = J(안정/정착)
        -- DataKnows AI 변동성 우선 사용 (RICHGO 폴백)
        ROUND((
            (f.jp_price_cv - s.m_pcv) / NULLIF(s.s_pcv, 0) +
            (f.young_ratio - s.m_yr)  / NULLIF(s.s_yr, 0)
        ) / 2, 4) AS jp_score

    FROM features f
    CROSS JOIN stats s
)

SELECT
    SGG,
    EMD,
    CITY_CODE,
    DISTRICT_CODE,
    ei_score,
    sn_score,
    tf_score,
    jp_score,
    -- MBTI 4글자 판정
    CASE WHEN ei_score >= 0 THEN 'E' ELSE 'I' END ||
    CASE WHEN sn_score >= 0 THEN 'S' ELSE 'N' END ||
    CASE WHEN tf_score >= 0 THEN 'T' ELSE 'F' END ||
    CASE WHEN jp_score >= 0 THEN 'P' ELSE 'J' END AS mbti,
    -- 각 축 강도 (절댓값)
    ABS(ei_score) AS ei_strength,
    ABS(sn_score) AS sn_strength,
    ABS(tf_score) AS tf_strength,
    ABS(jp_score) AS jp_strength
FROM scored
ORDER BY SGG, EMD;


-- ========================================
-- 검증 1: 동별 MBTI 확인
-- ========================================
SELECT SGG, EMD, mbti, ei_score, sn_score, tf_score, jp_score
FROM DONG_MBTI_RESULT
ORDER BY SGG, EMD;

-- ========================================
-- 검증 2: MBTI 유형 분포 (16유형 목표)
-- ========================================
SELECT mbti, COUNT(*) AS dong_count,
    LISTAGG(SGG || ' ' || EMD, ', ') WITHIN GROUP (ORDER BY SGG, EMD) AS dong_list
FROM DONG_MBTI_RESULT
GROUP BY mbti
ORDER BY dong_count DESC;
-- 기대: 최대한 다양한 유형 분포

-- ========================================
-- 검증 3: 축별 점수 분포 (정규분포 확인)
-- ========================================
SELECT
    'E/I' AS axis,
    MIN(ei_score) AS min_score,
    AVG(ei_score) AS avg_score,
    MAX(ei_score) AS max_score,
    STDDEV(ei_score) AS std_score
FROM DONG_MBTI_RESULT
UNION ALL
SELECT 'S/N', MIN(sn_score), AVG(sn_score), MAX(sn_score), STDDEV(sn_score)
FROM DONG_MBTI_RESULT
UNION ALL
SELECT 'T/F', MIN(tf_score), AVG(tf_score), MAX(tf_score), STDDEV(tf_score)
FROM DONG_MBTI_RESULT
UNION ALL
SELECT 'J/P', MIN(jp_score), AVG(jp_score), MAX(jp_score), STDDEV(jp_score)
FROM DONG_MBTI_RESULT;
-- 기대: 각 축 avg ≈ 0, std ≈ 0.5~1.5

-- ========================================
-- 검증 4: 구별 MBTI 분포 (편향 체크)
-- ========================================
SELECT SGG, mbti, COUNT(*) AS cnt
FROM DONG_MBTI_RESULT
GROUP BY SGG, mbti
ORDER BY SGG, cnt DESC;

-- ========================================
-- 검증 5: NULL 체크
-- ========================================
SELECT SGG, EMD, mbti, ei_score, sn_score, tf_score, jp_score
FROM DONG_MBTI_RESULT
WHERE mbti IS NULL OR ei_score IS NULL;
-- 기대: 0건
