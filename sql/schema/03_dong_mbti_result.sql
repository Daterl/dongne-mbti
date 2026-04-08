-- ============================================================
-- 03. DONG_MBTI_RESULT — 동별 MBTI 판정 테이블
-- v3: 3구 55동 딥다이브 — SPH + RICHGO 기반
-- z-score 정규화 → 4축 점수 → MBTI 4글자 판정
-- 의존: DONG_FEAT_EI, DONG_FEAT_SN, DONG_FEAT_TF, DONG_FEAT_JP
-- 크레딧: ~$0.01 (~55건 연산)
-- ============================================================
-- ⚠️ S/N 축: culture_ratio는 N 방향 → z-score 부호 반전
-- ⚠️ J/P 축: 2개 피처 (3개 아님)
-- ============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;

CREATE OR REPLACE TABLE DONG_MBTI_RESULT AS
WITH
-- 4축 피처 합치기
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
        -- S/N 피처 (SPH 카드소비)
        sn.practical_ratio,
        sn.edu_ratio,
        sn.culture_ratio,     -- ⚠️ N 방향: 부호 반전 필요
        -- T/F 피처 (SPH 자산 + RICHGO 시세)
        tf.avg_income,
        tf.avg_asset,
        tf.avg_price,
        -- J/P 피처 (RICHGO 변동성)
        jp.price_cv,
        jp.young_ratio
    FROM DONG_FEAT_EI ei
    JOIN DONG_FEAT_SN sn ON ei.DISTRICT_CODE = sn.DISTRICT_CODE
    JOIN DONG_FEAT_TF tf ON ei.DISTRICT_CODE = tf.DISTRICT_CODE
    JOIN DONG_FEAT_JP jp ON ei.DISTRICT_CODE = jp.DISTRICT_CODE
),

-- z-score 정규화용 통계
stats AS (
    SELECT
        -- E/I
        AVG(visit_ratio) AS m_vr, STDDEV(visit_ratio) AS s_vr,
        AVG(weekend_ratio) AS m_wr, STDDEV(weekend_ratio) AS s_wr,
        AVG(ent_ratio) AS m_er, STDDEV(ent_ratio) AS s_er,
        -- S/N
        AVG(practical_ratio) AS m_pr, STDDEV(practical_ratio) AS s_pr,
        AVG(edu_ratio) AS m_edr, STDDEV(edu_ratio) AS s_edr,
        AVG(culture_ratio) AS m_cr, STDDEV(culture_ratio) AS s_cr,
        -- T/F
        AVG(avg_income) AS m_ai, STDDEV(avg_income) AS s_ai,
        AVG(avg_asset) AS m_aa, STDDEV(avg_asset) AS s_aa,
        AVG(avg_price) AS m_ap, STDDEV(avg_price) AS s_ap,
        -- J/P
        AVG(price_cv) AS m_pcv, STDDEV(price_cv) AS s_pcv,
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
        -- 3개 피처 모두 E 방향
        ROUND((
            (f.visit_ratio - s.m_vr) / NULLIF(s.s_vr, 0) +
            (f.weekend_ratio - s.m_wr) / NULLIF(s.s_wr, 0) +
            (f.ent_ratio - s.m_er) / NULLIF(s.s_er, 0)
        ) / 3, 4) AS ei_score,

        -- S/N 점수: 양수 = S(실용/가정), 음수 = N(문화/개인)
        -- practical_ratio, edu_ratio → S 방향 (+)
        -- culture_ratio → N 방향 (−) ← 부호 반전!
        ROUND((
            (f.practical_ratio - s.m_pr) / NULLIF(s.s_pr, 0) +
            (f.edu_ratio - s.m_edr) / NULLIF(s.s_edr, 0) -
            (f.culture_ratio - s.m_cr) / NULLIF(s.s_cr, 0)
        ) / 3, 4) AS sn_score,

        -- T/F 점수: 양수 = T(경제/부유), 음수 = F(서민/생활)
        -- 3개 피처 모두 T 방향
        ROUND((
            (f.avg_income - s.m_ai) / NULLIF(s.s_ai, 0) +
            (f.avg_asset - s.m_aa) / NULLIF(s.s_aa, 0) +
            (f.avg_price - s.m_ap) / NULLIF(s.s_ap, 0)
        ) / 3, 4) AS tf_score,

        -- J/P 점수: 양수 = P(변화/유동), 음수 = J(안정/정착)
        -- 2개 피처 모두 P 방향
        ROUND((
            (f.price_cv - s.m_pcv) / NULLIF(s.s_pcv, 0) +
            (f.young_ratio - s.m_yr) / NULLIF(s.s_yr, 0)
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
    -- 각 축 강도 (절댓값, 0~3 범위)
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
-- 한 구에 하나의 MBTI만 몰리면 피처 다양성 부족 신호

-- ========================================
-- 검증 5: NULL 체크 (MBTI가 NULL인 동)
-- ========================================
SELECT SGG, EMD, mbti, ei_score, sn_score, tf_score, jp_score
FROM DONG_MBTI_RESULT
WHERE mbti IS NULL OR ei_score IS NULL;
-- 기대: 0건
