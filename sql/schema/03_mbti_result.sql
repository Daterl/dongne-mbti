-- ============================================================
-- 03. GU_MBTI_RESULT — 구별 MBTI 판정 테이블
-- v2: RICHGO(25구) + Telecom(25구) 기반 재설계
-- z-score 정규화 → 4축 점수 → MBTI 4글자 판정
-- 의존: GU_FEAT_EI, GU_FEAT_SN, GU_FEAT_TF, GU_FEAT_JP
-- 크레딧: ~$0.01 (25건 연산)
-- ============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;

CREATE OR REPLACE TABLE GU_MBTI_RESULT AS
WITH
-- 4축 피처 합치기
features AS (
    SELECT
        ei.SGG,
        ei.SGG_EN,
        ei.CITY_CODE,
        -- E/I 피처 (Telecom 활동성)
        ei.contract_density,
        ei.new_install_rate,
        ei.consult_ratio,
        -- S/N 피처 (RICHGO 라이프스타일)
        sn.jeonse_ratio,
        sn.child_ratio,
        sn.household_density,
        -- T/F 피처 (RICHGO 경제 + Telecom 지출)
        tf.avg_price,
        tf.avg_net_sales,
        tf.bundle_ratio,
        -- J/P 피처 (변동성)
        jp.price_cv,
        jp.young_ratio,
        jp.contract_cv
    FROM GU_FEAT_EI ei
    JOIN GU_FEAT_SN sn ON ei.CITY_CODE = sn.CITY_CODE
    JOIN GU_FEAT_TF tf ON ei.CITY_CODE = tf.CITY_CODE
    JOIN GU_FEAT_JP jp ON ei.CITY_CODE = jp.CITY_CODE
),

-- z-score 정규화용 통계
stats AS (
    SELECT
        -- E/I
        AVG(contract_density) AS m_cd, STDDEV(contract_density) AS s_cd,
        AVG(new_install_rate) AS m_nir, STDDEV(new_install_rate) AS s_nir,
        AVG(consult_ratio) AS m_cr, STDDEV(consult_ratio) AS s_cr,
        -- S/N
        AVG(jeonse_ratio) AS m_jr, STDDEV(jeonse_ratio) AS s_jr,
        AVG(child_ratio) AS m_chr, STDDEV(child_ratio) AS s_chr,
        AVG(household_density) AS m_hd, STDDEV(household_density) AS s_hd,
        -- T/F
        AVG(avg_price) AS m_ap, STDDEV(avg_price) AS s_ap,
        AVG(avg_net_sales) AS m_ans, STDDEV(avg_net_sales) AS s_ans,
        AVG(bundle_ratio) AS m_br, STDDEV(bundle_ratio) AS s_br,
        -- J/P
        AVG(price_cv) AS m_pcv, STDDEV(price_cv) AS s_pcv,
        AVG(young_ratio) AS m_yr, STDDEV(young_ratio) AS s_yr,
        AVG(contract_cv) AS m_ccv, STDDEV(contract_cv) AS s_ccv
    FROM features
),

-- z-score 적용 + 축별 점수 계산
scored AS (
    SELECT
        f.SGG,
        f.SGG_EN,
        f.CITY_CODE,

        -- E/I 점수: 양수 = E(외향/활동), 음수 = I(내향/조용)
        ROUND((
            (f.contract_density - s.m_cd) / NULLIF(s.s_cd, 0) +
            (f.new_install_rate - s.m_nir) / NULLIF(s.s_nir, 0) +
            (f.consult_ratio - s.m_cr) / NULLIF(s.s_cr, 0)
        ) / 3, 4) AS ei_score,

        -- S/N 점수: 양수 = S(실용/가정), 음수 = N(문화/개인)
        ROUND((
            (f.jeonse_ratio - s.m_jr) / NULLIF(s.s_jr, 0) +
            (f.child_ratio - s.m_chr) / NULLIF(s.s_chr, 0) +
            (f.household_density - s.m_hd) / NULLIF(s.s_hd, 0)
        ) / 3, 4) AS sn_score,

        -- T/F 점수: 양수 = T(경제/부유), 음수 = F(서민/생활)
        ROUND((
            (f.avg_price - s.m_ap) / NULLIF(s.s_ap, 0) +
            (f.avg_net_sales - s.m_ans) / NULLIF(s.s_ans, 0) +
            (f.bundle_ratio - s.m_br) / NULLIF(s.s_br, 0)
        ) / 3, 4) AS tf_score,

        -- J/P 점수: 양수 = P(변화/유동), 음수 = J(안정/정착)
        ROUND((
            (f.price_cv - s.m_pcv) / NULLIF(s.s_pcv, 0) +
            (f.young_ratio - s.m_yr) / NULLIF(s.s_yr, 0) +
            (f.contract_cv - s.m_ccv) / NULLIF(s.s_ccv, 0)
        ) / 3, 4) AS jp_score

    FROM features f
    CROSS JOIN stats s
)

SELECT
    SGG,
    SGG_EN,
    CITY_CODE,
    ei_score,
    sn_score,
    tf_score,
    jp_score,
    -- MBTI 4글자 판정
    CASE WHEN ei_score >= 0 THEN 'E' ELSE 'I' END ||
    CASE WHEN sn_score >= 0 THEN 'S' ELSE 'N' END ||
    CASE WHEN tf_score >= 0 THEN 'T' ELSE 'F' END ||
    CASE WHEN jp_score >= 0 THEN 'P' ELSE 'J' END AS mbti,
    -- 각 축 강도 (절댓값, 0~1+ 범위)
    ABS(ei_score) AS ei_strength,
    ABS(sn_score) AS sn_strength,
    ABS(tf_score) AS tf_strength,
    ABS(jp_score) AS jp_strength
FROM scored
ORDER BY SGG;

-- 검증: 구별 MBTI 확인
SELECT SGG, mbti, ei_score, sn_score, tf_score, jp_score
FROM GU_MBTI_RESULT
ORDER BY SGG;

-- MBTI 유형 분포
SELECT mbti, COUNT(*) AS gu_count, LISTAGG(SGG, ', ') AS gu_list
FROM GU_MBTI_RESULT
GROUP BY mbti
ORDER BY gu_count DESC;
