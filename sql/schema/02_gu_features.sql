-- ============================================================
-- 02. GU_FEATURES — 구 단위 MBTI 4축 피처 테이블
-- v2: SPH 3구 제한 해결 → RICHGO(25구) + Telecom V01/V05(25구) 전면 재설계
-- 의존: DONGNE_MASTER, RICHGO 3개 테이블, Telecom V01/V05
-- 크레딧: ~$0.05 (집계 쿼리만)
-- ============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;

-- ========================================
-- Step 1: E/I 축 피처 (Telecom 활동성)
-- 양수 = E(외향/활동적), 음수 = I(내향/조용한)
-- ========================================
CREATE OR REPLACE TABLE GU_FEAT_EI AS
WITH
-- V01: 구별 월평균 총계약 + 상담요청
telecom_v01 AS (
    SELECT
        INSTALL_CITY AS SGG,
        ROUND(AVG(monthly_contracts), 2) AS avg_monthly_contracts,
        ROUND(AVG(monthly_consults), 2) AS avg_monthly_consults
    FROM (
        SELECT
            INSTALL_CITY,
            YEAR_MONTH,
            SUM(CONTRACT_COUNT) AS monthly_contracts,
            SUM(CONSULT_REQUEST_COUNT) AS monthly_consults
        FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
            .TELECOM_INSIGHTS.V01_MONTHLY_REGIONAL_CONTRACT_STATS
        WHERE INSTALL_STATE = '서울'
        GROUP BY INSTALL_CITY, YEAR_MONTH
    )
    GROUP BY INSTALL_CITY
),
-- V05: 구별 월평균 신규설치
telecom_v05 AS (
    SELECT
        INSTALL_CITY AS SGG,
        ROUND(AVG(CONTRACT_COUNT), 2) AS avg_new_installs
    FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
        .TELECOM_INSIGHTS.V05_REGIONAL_NEW_INSTALL
    WHERE INSTALL_STATE = '서울'
    GROUP BY INSTALL_CITY
),
-- RICHGO 인구: 정규화용
population AS (
    SELECT
        SGG,
        ROUND(AVG(TOTAL), 0) AS avg_population
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_MOIS_POPULATION_GENDER_AGE_M_H
    WHERE SD = '서울'
    GROUP BY SGG
)
SELECT
    d.SGG,
    d.SGG_EN,
    d.CITY_CODE,
    -- 계약밀도: 월평균 계약건수 / 인구 → E 방향
    ROUND(v01.avg_monthly_contracts / NULLIF(pop.avg_population, 0), 6) AS contract_density,
    -- 신규설치율: 월평균 신규설치 / 인구 → E 방향
    ROUND(v05.avg_new_installs / NULLIF(pop.avg_population, 0), 6) AS new_install_rate,
    -- 상담비율: 상담요청 / 계약건수 → E 방향 (적극적 문의)
    ROUND(v01.avg_monthly_consults / NULLIF(v01.avg_monthly_contracts, 0), 4) AS consult_ratio
FROM (SELECT DISTINCT SGG, SGG_EN, CITY_CODE FROM DONGNE_MASTER) d
LEFT JOIN telecom_v01 v01 ON d.SGG = v01.SGG
LEFT JOIN telecom_v05 v05 ON d.SGG = v05.SGG
LEFT JOIN population pop ON d.SGG = pop.SGG;


-- ========================================
-- Step 2: S/N 축 피처 (RICHGO 라이프스타일)
-- 양수 = S(실용/가정), 음수 = N(문화/개인)
-- ========================================
CREATE OR REPLACE TABLE GU_FEAT_SN AS
WITH
richgo_price AS (
    SELECT
        SGG,
        ROUND(
            AVG(JEONSE_PRICE_PER_SUPPLY_PYEONG) /
            NULLIF(AVG(MEME_PRICE_PER_SUPPLY_PYEONG), 0), 4
        ) AS jeonse_ratio,
        ROUND(AVG(TOTAL_HOUSEHOLDS), 0) AS avg_households
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_APT_RICHGO_MARKET_PRICE_M_H
    WHERE SD = '서울'
      AND MEME_PRICE_PER_SUPPLY_PYEONG > 0
    GROUP BY SGG
),
richgo_child AS (
    SELECT
        SGG,
        ROUND(AVG(AGE_UNDER5_PER_FEMALE_20TO40), 4) AS child_ratio
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_MOIS_POPULATION_AGE_UNDER5_PER_FEMALE_20TO40_M_H
    WHERE SD = '서울'
    GROUP BY SGG
),
richgo_pop AS (
    SELECT
        SGG,
        ROUND(AVG(TOTAL), 0) AS avg_population
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_MOIS_POPULATION_GENDER_AGE_M_H
    WHERE SD = '서울'
    GROUP BY SGG
)
SELECT
    d.SGG,
    d.SGG_EN,
    d.CITY_CODE,
    -- 전세가율: 전세/매매 → S 방향 (실거주 중심)
    rp.jeonse_ratio,
    -- 영유아 비율 → S 방향 (가정중심)
    rc.child_ratio,
    -- 세대밀도: 세대수/인구 → S 방향 (소형가구 밀집 = 실용적)
    ROUND(rp.avg_households / NULLIF(pop.avg_population, 0), 4) AS household_density
FROM (SELECT DISTINCT SGG, SGG_EN, CITY_CODE FROM DONGNE_MASTER) d
LEFT JOIN richgo_price rp ON d.SGG = rp.SGG
LEFT JOIN richgo_child rc ON d.SGG = rc.SGG
LEFT JOIN richgo_pop pop ON d.SGG = pop.SGG;


-- ========================================
-- Step 3: T/F 축 피처 (RICHGO 경제 + Telecom 지출)
-- 양수 = T(경제/부유), 음수 = F(서민/생활)
-- ========================================
CREATE OR REPLACE TABLE GU_FEAT_TF AS
WITH
richgo_price AS (
    SELECT
        SGG,
        ROUND(AVG(MEME_PRICE_PER_SUPPLY_PYEONG), 0) AS avg_price
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_APT_RICHGO_MARKET_PRICE_M_H
    WHERE SD = '서울'
      AND MEME_PRICE_PER_SUPPLY_PYEONG > 0
    GROUP BY SGG
),
telecom_v05 AS (
    SELECT
        INSTALL_CITY AS SGG,
        ROUND(AVG(AVG_NET_SALES), 0) AS avg_net_sales,
        ROUND(
            AVG(BUNDLE_COUNT) /
            NULLIF(AVG(BUNDLE_COUNT) + AVG(STANDALONE_COUNT), 0), 4
        ) AS bundle_ratio
    FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
        .TELECOM_INSIGHTS.V05_REGIONAL_NEW_INSTALL
    WHERE INSTALL_STATE = '서울'
    GROUP BY INSTALL_CITY
)
SELECT
    d.SGG,
    d.SGG_EN,
    d.CITY_CODE,
    -- 매매 평당가 → T 방향 (부동산 경제력)
    rp.avg_price,
    -- 통신 평균 순매출 → T 방향 (지출 수준)
    v05.avg_net_sales,
    -- 번들 가입비율 → T 방향 (다중서비스 = 경제력)
    v05.bundle_ratio
FROM (SELECT DISTINCT SGG, SGG_EN, CITY_CODE FROM DONGNE_MASTER) d
LEFT JOIN richgo_price rp ON d.SGG = rp.SGG
LEFT JOIN telecom_v05 v05 ON d.SGG = v05.SGG;


-- ========================================
-- Step 4: J/P 축 피처 (RICHGO 변동성 + Telecom 변동성)
-- 양수 = P(변화/유동), 음수 = J(안정/정착)
-- ========================================
CREATE OR REPLACE TABLE GU_FEAT_JP AS
WITH
price_vol AS (
    SELECT
        SGG,
        ROUND(
            STDDEV(MEME_PRICE_PER_SUPPLY_PYEONG) /
            NULLIF(AVG(MEME_PRICE_PER_SUPPLY_PYEONG), 0), 4
        ) AS price_cv
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_APT_RICHGO_MARKET_PRICE_M_H
    WHERE SD = '서울'
    GROUP BY SGG
),
young_pop AS (
    SELECT
        SGG,
        ROUND(SUM(AGE_20S + AGE_30S) / NULLIF(SUM(TOTAL), 0), 4) AS young_ratio
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_MOIS_POPULATION_GENDER_AGE_M_H
    WHERE SD = '서울'
    GROUP BY SGG
),
-- V01: 구별 월별 계약 변동성 (CV)
contract_vol AS (
    SELECT
        INSTALL_CITY AS SGG,
        ROUND(
            STDDEV(monthly_contracts) /
            NULLIF(AVG(monthly_contracts), 0), 4
        ) AS contract_cv
    FROM (
        SELECT
            INSTALL_CITY,
            YEAR_MONTH,
            SUM(CONTRACT_COUNT) AS monthly_contracts
        FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
            .TELECOM_INSIGHTS.V01_MONTHLY_REGIONAL_CONTRACT_STATS
        WHERE INSTALL_STATE = '서울'
        GROUP BY INSTALL_CITY, YEAR_MONTH
    )
    GROUP BY INSTALL_CITY
)
SELECT
    d.SGG,
    d.SGG_EN,
    d.CITY_CODE,
    -- 시세 변동성 → P 방향
    pv.price_cv,
    -- 20-30대 비율 → P 방향 (젊은층 = 유동적)
    yp.young_ratio,
    -- 계약 변동성 → P 방향 (수요 변동)
    cv.contract_cv
FROM (SELECT DISTINCT SGG, SGG_EN, CITY_CODE FROM DONGNE_MASTER) d
LEFT JOIN price_vol pv ON d.SGG = pv.SGG
LEFT JOIN young_pop yp ON d.SGG = yp.SGG
LEFT JOIN contract_vol cv ON d.SGG = cv.SGG;


-- ========================================
-- 검증: 4개 피처 테이블 행 수 + NULL 체크
-- ========================================
SELECT 'GU_FEAT_EI' AS tbl, COUNT(*) AS cnt,
    COUNT(*) - COUNT(contract_density) AS null_cd,
    COUNT(*) - COUNT(new_install_rate) AS null_nir,
    COUNT(*) - COUNT(consult_ratio) AS null_cr
FROM GU_FEAT_EI
UNION ALL
SELECT 'GU_FEAT_SN', COUNT(*),
    COUNT(*) - COUNT(jeonse_ratio),
    COUNT(*) - COUNT(child_ratio),
    COUNT(*) - COUNT(household_density)
FROM GU_FEAT_SN
UNION ALL
SELECT 'GU_FEAT_TF', COUNT(*),
    COUNT(*) - COUNT(avg_price),
    COUNT(*) - COUNT(avg_net_sales),
    COUNT(*) - COUNT(bundle_ratio)
FROM GU_FEAT_TF
UNION ALL
SELECT 'GU_FEAT_JP', COUNT(*),
    COUNT(*) - COUNT(price_cv),
    COUNT(*) - COUNT(young_ratio),
    COUNT(*) - COUNT(contract_cv)
FROM GU_FEAT_JP;
-- 기대: 각 25건, NULL 0

-- JOIN 키 매칭 확인: Telecom INSTALL_CITY vs DONGNE_MASTER SGG
SELECT v.INSTALL_CITY, d.SGG
FROM (
    SELECT DISTINCT INSTALL_CITY
    FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
        .TELECOM_INSIGHTS.V01_MONTHLY_REGIONAL_CONTRACT_STATS
    WHERE INSTALL_STATE = '서울'
) v
FULL OUTER JOIN (SELECT DISTINCT SGG FROM DONGNE_MASTER) d
    ON v.INSTALL_CITY = d.SGG
WHERE v.INSTALL_CITY IS NULL OR d.SGG IS NULL;
-- 기대: 0건 (완전 매칭)
