-- ============================================================
-- 02. DONG_FEATURES — 동 단위 MBTI 4축 피처 테이블
-- v3: 3구 55동 딥다이브 — SPH(동 단위) + RICHGO(동/구 단위)
-- 대상: 서초구, 영등포구, 중구
-- 의존: DONGNE_MASTER
-- 크레딧: ~$0.05 (집계 쿼리만)
-- ============================================================
-- SPH DB: SEOUL_DISTRICTLEVEL_DATA_FLOATING_POPULATION_CONSUMPTION_AND_ASSETS.GRANDATA
-- RICHGO DB: KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA.HACKATHON_2025Q2
-- ============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;

-- ========================================
-- Step 0: 3구 동 목록 확인
-- ========================================
SELECT SGG, COUNT(*) AS dong_count
FROM DONGNE_MASTER
WHERE SGG IN ('서초구', '영등포구', '중구')
GROUP BY SGG
ORDER BY SGG;
-- 기대: 3구, 합계 ~55동


-- ========================================
-- Step 1: E/I 축 피처 (SPH 유동인구 + 카드소비)
-- 양수 = E(외향/활동적), 음수 = I(내향/조용한)
-- ========================================
CREATE OR REPLACE TABLE DONG_FEAT_EI AS
WITH
-- 동별 유동인구 집계 (전 시간대/연령/성별 합산)
pop_agg AS (
    SELECT
        fp.DISTRICT_CODE,
        -- 방문인구 비율: 방문객 많을수록 E
        ROUND(SUM(fp.VISITING_POPULATION) /
            NULLIF(SUM(fp.RESIDENTIAL_POPULATION), 0), 4) AS visit_ratio,
        -- 주말 활동 비율: 주말 유동인구 비중 높을수록 E
        ROUND(
            SUM(CASE WHEN fp.WEEKDAY_WEEKEND IN ('WEEKEND', '주말')
                THEN fp.VISITING_POPULATION + fp.WORKING_POPULATION + fp.RESIDENTIAL_POPULATION
                ELSE 0 END) /
            NULLIF(SUM(fp.VISITING_POPULATION + fp.WORKING_POPULATION + fp.RESIDENTIAL_POPULATION), 0)
        , 4) AS weekend_ratio
    FROM SEOUL_DISTRICTLEVEL_DATA_FLOATING_POPULATION_CONSUMPTION_AND_ASSETS
        .GRANDATA.FLOATING_POPULATION_INFO fp
    INNER JOIN DONGNE_MASTER d
        ON fp.CITY_CODE = d.CITY_CODE AND fp.DISTRICT_CODE = d.DISTRICT_CODE
    WHERE d.SGG IN ('서초구', '영등포구', '중구')
    GROUP BY fp.DISTRICT_CODE
),
-- 동별 엔터테인먼트/문화 소비 비중
card_ent AS (
    SELECT
        cs.DISTRICT_CODE,
        -- 오락+문화레저 소비 비중: 높을수록 E
        ROUND(
            SUM(cs.ENTERTAINMENT_SALES + cs.SPORTS_CULTURE_LEISURE_SALES) /
            NULLIF(SUM(cs.TOTAL_SALES), 0)
        , 4) AS ent_ratio
    FROM SEOUL_DISTRICTLEVEL_DATA_FLOATING_POPULATION_CONSUMPTION_AND_ASSETS
        .GRANDATA.CARD_SALES_INFO cs
    INNER JOIN DONGNE_MASTER d
        ON cs.CITY_CODE = d.CITY_CODE AND cs.DISTRICT_CODE = d.DISTRICT_CODE
    WHERE d.SGG IN ('서초구', '영등포구', '중구')
    GROUP BY cs.DISTRICT_CODE
)
SELECT
    d.SGG,
    d.EMD,
    d.CITY_CODE,
    d.DISTRICT_CODE,
    p.visit_ratio,      -- E 방향: 방문인구 / 거주인구
    p.weekend_ratio,     -- E 방향: 주말 활동 비중
    c.ent_ratio          -- E 방향: 오락+문화 소비 비중
FROM DONGNE_MASTER d
LEFT JOIN pop_agg p ON d.DISTRICT_CODE = p.DISTRICT_CODE
LEFT JOIN card_ent c ON d.DISTRICT_CODE = c.DISTRICT_CODE
WHERE d.SGG IN ('서초구', '영등포구', '중구');


-- ========================================
-- Step 2: S/N 축 피처 (SPH 카드소비 패턴)
-- 양수 = S(실용/가정), 음수 = N(문화/개인)
-- ⚠️ culture_ratio는 N 방향 (03에서 z-score 부호 반전)
-- ========================================
CREATE OR REPLACE TABLE DONG_FEAT_SN AS
WITH
card_agg AS (
    SELECT
        cs.DISTRICT_CODE,
        -- 생필품 소비 비중 → S 방향 (식품+의료)
        ROUND(
            SUM(cs.FOOD_SALES + cs.MEDICAL_SALES) /
            NULLIF(SUM(cs.TOTAL_SALES), 0)
        , 4) AS practical_ratio,
        -- 교육 소비 비중 → S 방향 (학원/교육)
        ROUND(
            SUM(cs.EDUCATION_ACADEMY_SALES) /
            NULLIF(SUM(cs.TOTAL_SALES), 0)
        , 4) AS edu_ratio,
        -- 문화/카페 소비 비중 → N 방향 (03에서 부호 반전)
        ROUND(
            SUM(cs.COFFEE_SALES + cs.ENTERTAINMENT_SALES + cs.SPORTS_CULTURE_LEISURE_SALES) /
            NULLIF(SUM(cs.TOTAL_SALES), 0)
        , 4) AS culture_ratio
    FROM SEOUL_DISTRICTLEVEL_DATA_FLOATING_POPULATION_CONSUMPTION_AND_ASSETS
        .GRANDATA.CARD_SALES_INFO cs
    INNER JOIN DONGNE_MASTER d
        ON cs.CITY_CODE = d.CITY_CODE AND cs.DISTRICT_CODE = d.DISTRICT_CODE
    WHERE d.SGG IN ('서초구', '영등포구', '중구')
    GROUP BY cs.DISTRICT_CODE
)
SELECT
    d.SGG,
    d.EMD,
    d.CITY_CODE,
    d.DISTRICT_CODE,
    c.practical_ratio,   -- S 방향: 생필품(식품+의료) 소비 비중
    c.edu_ratio,         -- S 방향: 교육/학원 소비 비중
    c.culture_ratio      -- ⚠️ N 방향: 문화(커피+오락+레저) 소비 비중
FROM DONGNE_MASTER d
LEFT JOIN card_agg c ON d.DISTRICT_CODE = c.DISTRICT_CODE
WHERE d.SGG IN ('서초구', '영등포구', '중구');


-- ========================================
-- Step 3: T/F 축 피처 (SPH 자산소득 + RICHGO 시세)
-- 양수 = T(경제/부유), 음수 = F(서민/생활)
-- ========================================
CREATE OR REPLACE TABLE DONG_FEAT_TF AS
WITH
-- SPH 자산/소득 (동별)
asset_agg AS (
    SELECT
        ai.DISTRICT_CODE,
        ROUND(AVG(ai.AVERAGE_INCOME), 0) AS avg_income,
        ROUND(AVG(ai.AVERAGE_ASSET_AMOUNT), 0) AS avg_asset
    FROM SEOUL_DISTRICTLEVEL_DATA_FLOATING_POPULATION_CONSUMPTION_AND_ASSETS
        .GRANDATA.ASSET_INCOME_INFO ai
    INNER JOIN DONGNE_MASTER d
        ON ai.CITY_CODE = d.CITY_CODE AND ai.DISTRICT_CODE = d.DISTRICT_CODE
    WHERE d.SGG IN ('서초구', '영등포구', '중구')
    GROUP BY ai.DISTRICT_CODE
),
-- RICHGO 매매 평당가 (동 단위 시도, 실패 시 구 단위 대체)
richgo_price AS (
    SELECT
        rp.SGG,
        rp.EMD,
        ROUND(AVG(rp.MEME_PRICE_PER_SUPPLY_PYEONG), 0) AS avg_price
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_APT_RICHGO_MARKET_PRICE_M_H rp
    WHERE rp.SD = '서울'
      AND rp.SGG IN ('서초구', '영등포구', '중구')
      AND rp.MEME_PRICE_PER_SUPPLY_PYEONG > 0
    GROUP BY rp.SGG, rp.EMD
),
-- RICHGO 구 단위 평균 (동 매칭 실패 시 폴백)
richgo_price_gu AS (
    SELECT
        rp.SGG,
        ROUND(AVG(rp.MEME_PRICE_PER_SUPPLY_PYEONG), 0) AS avg_price_gu
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_APT_RICHGO_MARKET_PRICE_M_H rp
    WHERE rp.SD = '서울'
      AND rp.SGG IN ('서초구', '영등포구', '중구')
      AND rp.MEME_PRICE_PER_SUPPLY_PYEONG > 0
    GROUP BY rp.SGG
)
SELECT
    d.SGG,
    d.EMD,
    d.CITY_CODE,
    d.DISTRICT_CODE,
    a.avg_income,        -- T 방향: 평균 소득 (SPH)
    a.avg_asset,         -- T 방향: 평균 자산 (SPH)
    COALESCE(rp.avg_price, rpg.avg_price_gu) AS avg_price  -- T 방향: 매매 평당가 (RICHGO 동→구 폴백)
FROM DONGNE_MASTER d
LEFT JOIN asset_agg a ON d.DISTRICT_CODE = a.DISTRICT_CODE
LEFT JOIN richgo_price rp ON d.SGG = rp.SGG AND d.EMD = rp.EMD
LEFT JOIN richgo_price_gu rpg ON d.SGG = rpg.SGG
WHERE d.SGG IN ('서초구', '영등포구', '중구');


-- ========================================
-- Step 4: J/P 축 피처 (RICHGO 변동성 + 인구구조)
-- 양수 = P(변화/유동), 음수 = J(안정/정착)
-- ========================================
CREATE OR REPLACE TABLE DONG_FEAT_JP AS
WITH
-- 시세 변동성 (CV = 변동계수): 동 단위 시도 → 구 폴백
price_vol_dong AS (
    SELECT
        rp.SGG,
        rp.EMD,
        ROUND(
            STDDEV(rp.MEME_PRICE_PER_SUPPLY_PYEONG) /
            NULLIF(AVG(rp.MEME_PRICE_PER_SUPPLY_PYEONG), 0)
        , 4) AS price_cv
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_APT_RICHGO_MARKET_PRICE_M_H rp
    WHERE rp.SD = '서울'
      AND rp.SGG IN ('서초구', '영등포구', '중구')
      AND rp.MEME_PRICE_PER_SUPPLY_PYEONG > 0
    GROUP BY rp.SGG, rp.EMD
),
price_vol_gu AS (
    SELECT
        rp.SGG,
        ROUND(
            STDDEV(rp.MEME_PRICE_PER_SUPPLY_PYEONG) /
            NULLIF(AVG(rp.MEME_PRICE_PER_SUPPLY_PYEONG), 0)
        , 4) AS price_cv_gu
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_APT_RICHGO_MARKET_PRICE_M_H rp
    WHERE rp.SD = '서울'
      AND rp.SGG IN ('서초구', '영등포구', '중구')
    GROUP BY rp.SGG
),
-- 20-30대 비율: 동 단위 시도 → 구 폴백
young_dong AS (
    SELECT
        pop.SGG,
        pop.EMD,
        ROUND(SUM(pop.AGE_20S + pop.AGE_30S) / NULLIF(SUM(pop.TOTAL), 0), 4) AS young_ratio
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_MOIS_POPULATION_GENDER_AGE_M_H pop
    WHERE pop.SD = '서울'
      AND pop.SGG IN ('서초구', '영등포구', '중구')
    GROUP BY pop.SGG, pop.EMD
),
young_gu AS (
    SELECT
        pop.SGG,
        ROUND(SUM(pop.AGE_20S + pop.AGE_30S) / NULLIF(SUM(pop.TOTAL), 0), 4) AS young_ratio_gu
    FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
        .HACKATHON_2025Q2.REGION_MOIS_POPULATION_GENDER_AGE_M_H pop
    WHERE pop.SD = '서울'
      AND pop.SGG IN ('서초구', '영등포구', '중구')
    GROUP BY pop.SGG
)
SELECT
    d.SGG,
    d.EMD,
    d.CITY_CODE,
    d.DISTRICT_CODE,
    COALESCE(pvd.price_cv, pvg.price_cv_gu) AS price_cv,      -- P 방향: 시세 변동성
    COALESCE(yd.young_ratio, yg.young_ratio_gu) AS young_ratio -- P 방향: 20-30대 비율
FROM DONGNE_MASTER d
LEFT JOIN price_vol_dong pvd ON d.SGG = pvd.SGG AND d.EMD = pvd.EMD
LEFT JOIN price_vol_gu pvg ON d.SGG = pvg.SGG
LEFT JOIN young_dong yd ON d.SGG = yd.SGG AND d.EMD = yd.EMD
LEFT JOIN young_gu yg ON d.SGG = yg.SGG
WHERE d.SGG IN ('서초구', '영등포구', '중구');


-- ========================================
-- 검증: 4개 피처 테이블 행 수 + NULL 체크
-- ========================================
SELECT 'DONG_FEAT_EI' AS tbl, COUNT(*) AS cnt,
    COUNT(*) - COUNT(visit_ratio) AS null_visit,
    COUNT(*) - COUNT(weekend_ratio) AS null_weekend,
    COUNT(*) - COUNT(ent_ratio) AS null_ent
FROM DONG_FEAT_EI
UNION ALL
SELECT 'DONG_FEAT_SN', COUNT(*),
    COUNT(*) - COUNT(practical_ratio),
    COUNT(*) - COUNT(edu_ratio),
    COUNT(*) - COUNT(culture_ratio)
FROM DONG_FEAT_SN
UNION ALL
SELECT 'DONG_FEAT_TF', COUNT(*),
    COUNT(*) - COUNT(avg_income),
    COUNT(*) - COUNT(avg_asset),
    COUNT(*) - COUNT(avg_price)
FROM DONG_FEAT_TF
UNION ALL
SELECT 'DONG_FEAT_JP', COUNT(*),
    COUNT(*) - COUNT(price_cv),
    COUNT(*) - COUNT(young_ratio),
    0  -- J/P는 2개 피처
FROM DONG_FEAT_JP;
-- 기대: 각 ~55건, NULL 0 (SPH 3구 커버)
-- ⚠️ RICHGO 동 매칭이 불완전하면 avg_price, price_cv에 NULL 가능 → 구 폴백으로 커버

-- RICHGO 동 매칭률 확인
SELECT
    'T/F avg_price' AS feature,
    COUNT(*) AS total,
    COUNT(avg_price) AS matched,
    ROUND(COUNT(avg_price) * 100.0 / COUNT(*), 1) AS match_pct
FROM DONG_FEAT_TF
UNION ALL
SELECT
    'J/P price_cv',
    COUNT(*),
    COUNT(price_cv),
    ROUND(COUNT(price_cv) * 100.0 / COUNT(*), 1)
FROM DONG_FEAT_JP;
-- 기대: 100% (구 폴백이 작동하므로)
