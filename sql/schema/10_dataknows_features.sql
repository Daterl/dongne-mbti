-- =============================================================
-- 10_dataknows_features.sql
-- 이슈 #21: DataKnows 피처 추출 (역세권 + AI 시세 2026)
-- =============================================================
-- DataKnows Korea Real Estate Apartment Market Intelligence
-- DB: KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE.HACKATHON_2026
-- 의존: DONGNE_MASTER
-- 크레딧: ~$0.03 (집계 쿼리만, AI 호출 없음)
-- =============================================================
-- 신규 피처:
--   DONG_FEAT_SUBWAY   → S/N 축 보강 (역세권 = N 방향)
--   DONG_FEAT_DK_PRICE → T/F / J/P 축 업그레이드 (AI 시세 2026 최신)
-- =============================================================
-- 퍼지매칭 전략:
--   영등포구 "가(街)" 불일치 해결 — "당산동1가" → "당산동"
--   REGEXP_REPLACE(d.EMD, '[0-9]+가$', '') = source.EMD
-- 폴백 전략:
--   EMD 매칭 실패 시 SGG 레벨 평균 사용 (COALESCE)
-- =============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;


-- ========================================
-- Step 0: 매칭 현황 검증
-- ========================================
-- 정규화(퍼지) 매칭 후 커버율 확인
WITH normalized AS (
    SELECT
        d.SGG,
        d.EMD,
        REGEXP_REPLACE(d.EMD, '[0-9]+가$', '') AS emd_norm,
        CASE WHEN p.EMD IS NOT NULL THEN 'O' ELSE 'X' END AS price_exact,
        CASE WHEN pf.EMD IS NOT NULL THEN 'O' ELSE 'X' END AS price_fuzzy,
        CASE WHEN s.EMD IS NOT NULL THEN 'O' ELSE 'X' END AS subway_exact,
        CASE WHEN sf.EMD IS NOT NULL THEN 'O' ELSE 'X' END AS subway_fuzzy
    FROM DONGNE_MBTI.PUBLIC.DONGNE_MASTER d
    LEFT JOIN (
        SELECT DISTINCT SGG, EMD
        FROM KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE
             .HACKATHON_2026.REGION_APT_RICHGO_MARKET_PRICE_M_H
        WHERE REGION_LEVEL = 'emd' AND SGG IN ('서초구', '영등포구', '중구')
    ) p ON d.SGG = p.SGG AND d.EMD = p.EMD
    LEFT JOIN (
        SELECT DISTINCT SGG, EMD
        FROM KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE
             .HACKATHON_2026.REGION_APT_RICHGO_MARKET_PRICE_M_H
        WHERE REGION_LEVEL = 'emd' AND SGG IN ('서초구', '영등포구', '중구')
    ) pf ON d.SGG = pf.SGG AND REGEXP_REPLACE(d.EMD, '[0-9]+가$', '') = pf.EMD
    LEFT JOIN (
        SELECT DISTINCT SGG, EMD
        FROM KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE
             .HACKATHON_2026.APT_DANJI_AND_TRANSPORTATION_TRAIN_DISTANCE
        WHERE SGG IN ('서초구', '영등포구', '중구')
    ) s ON d.SGG = s.SGG AND d.EMD = s.EMD
    LEFT JOIN (
        SELECT DISTINCT SGG, EMD
        FROM KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE
             .HACKATHON_2026.APT_DANJI_AND_TRANSPORTATION_TRAIN_DISTANCE
        WHERE SGG IN ('서초구', '영등포구', '중구')
    ) sf ON d.SGG = sf.SGG AND REGEXP_REPLACE(d.EMD, '[0-9]+가$', '') = sf.EMD
    WHERE d.SGG IN ('서초구', '영등포구', '중구')
)
SELECT
    SGG,
    SUM(CASE WHEN price_exact = 'O' THEN 1 ELSE 0 END) AS price_exact_cnt,
    SUM(CASE WHEN price_fuzzy = 'O' THEN 1 ELSE 0 END) AS price_fuzzy_cnt,
    SUM(CASE WHEN subway_exact = 'O' THEN 1 ELSE 0 END) AS subway_exact_cnt,
    SUM(CASE WHEN subway_fuzzy = 'O' THEN 1 ELSE 0 END) AS subway_fuzzy_cnt,
    COUNT(*) AS total
FROM normalized
GROUP BY SGG
ORDER BY SGG;
-- 기대: 영등포구 price_fuzzy_cnt > price_exact_cnt (가(街) 매칭 개선 확인)


-- ========================================
-- Step 1: DONG_FEAT_SUBWAY — 역세권 피처
-- S/N 축 보강: avg_subway_distance_m 높을수록 S(주거/실용)
--             subway_access_ratio 높을수록 N(도시/문화)
-- ========================================
CREATE OR REPLACE TABLE DONG_FEAT_SUBWAY AS
WITH
-- 단지별 가장 가까운 지하철역 거리 (행 1개 = 단지 1개, 여러 역 중 최소 거리)
danji_nearest AS (
    SELECT
        SGG,
        EMD,
        DANJI_ID,
        MIN(DISTANCE) AS nearest_station_m
    FROM KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE
         .HACKATHON_2026.APT_DANJI_AND_TRANSPORTATION_TRAIN_DISTANCE
    WHERE SGG IN ('서초구', '영등포구', '중구')
    GROUP BY SGG, EMD, DANJI_ID
),
-- 가장 가까운 역의 월평균 승하차 (교통 활성도 지표)
danji_ridership AS (
    SELECT
        t.SGG,
        t.EMD,
        t.DANJI_ID,
        AVG(t.GET_ON + t.GET_OFF) AS avg_monthly_ridership
    FROM KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE
         .HACKATHON_2026.APT_DANJI_AND_TRANSPORTATION_TRAIN_DISTANCE t
    INNER JOIN danji_nearest dn
        ON t.SGG = dn.SGG AND t.EMD = dn.EMD AND t.DANJI_ID = dn.DANJI_ID
        AND t.DISTANCE = dn.nearest_station_m
    GROUP BY t.SGG, t.EMD, t.DANJI_ID
),
-- 단지 합산
danji_all AS (
    SELECT
        n.SGG,
        n.EMD,
        n.DANJI_ID,
        n.nearest_station_m,
        COALESCE(r.avg_monthly_ridership, 0) AS avg_ridership
    FROM danji_nearest n
    LEFT JOIN danji_ridership r
        ON n.SGG = r.SGG AND n.EMD = r.EMD AND n.DANJI_ID = r.DANJI_ID
),
-- EMD 단위 집계 (원본 EMD명 기준)
emd_subway AS (
    SELECT
        SGG,
        EMD,
        ROUND(AVG(nearest_station_m), 0)                                AS avg_subway_distance_m,
        ROUND(AVG(avg_ridership), 0)                                     AS avg_station_ridership,
        COUNT(DISTINCT DANJI_ID)                                         AS apt_danji_count,
        SUM(CASE WHEN nearest_station_m <= 500 THEN 1 ELSE 0 END)        AS danji_within_500m
    FROM danji_all
    GROUP BY SGG, EMD
),
-- SGG 레벨 폴백 (EMD 미매칭 동을 위한 구 단위 평균)
sgg_subway AS (
    SELECT
        SGG,
        ROUND(AVG(avg_subway_distance_m), 0)   AS avg_subway_distance_m_sgg,
        ROUND(AVG(avg_station_ridership), 0)   AS avg_station_ridership_sgg
    FROM emd_subway
    GROUP BY SGG
)
SELECT
    d.SGG,
    d.EMD,
    d.CITY_CODE,
    d.DISTRICT_CODE,

    -- 역세권 거리 (EMD 정확 매칭 → 퍼지 매칭 → SGG 폴백)
    COALESCE(
        se.avg_subway_distance_m,
        sf.avg_subway_distance_m,
        sg.avg_subway_distance_m_sgg
    )                                               AS avg_subway_distance_m,

    -- 월평균 승하차 (교통 활성도)
    COALESCE(
        se.avg_station_ridership,
        sf.avg_station_ridership,
        sg.avg_station_ridership_sgg
    )                                               AS avg_station_ridership,

    -- 아파트 단지 수 (0이면 해당 동 데이터 없음)
    COALESCE(se.apt_danji_count, sf.apt_danji_count, 0) AS apt_danji_count,

    -- 역세권 비율: 500m 이내 단지 / 전체 단지 (높을수록 N 방향)
    CASE
        WHEN COALESCE(se.apt_danji_count, sf.apt_danji_count, 0) > 0
        THEN ROUND(
            COALESCE(se.danji_within_500m, sf.danji_within_500m, 0) * 1.0 /
            COALESCE(se.apt_danji_count, sf.apt_danji_count, 1),
            4)
        ELSE NULL
    END                                             AS subway_access_ratio

FROM DONGNE_MBTI.PUBLIC.DONGNE_MASTER d

-- 1순위: 정확 매칭 (EMD = EMD)
LEFT JOIN emd_subway se
    ON d.SGG = se.SGG AND d.EMD = se.EMD

-- 2순위: 퍼지 매칭 (당산동1가 → 당산동)
LEFT JOIN emd_subway sf
    ON d.SGG = sf.SGG
    AND REGEXP_REPLACE(d.EMD, '[0-9]+가$', '') = sf.EMD
    AND se.EMD IS NULL   -- 정확 매칭 없을 때만 사용

-- 3순위: SGG 폴백
LEFT JOIN sgg_subway sg ON d.SGG = sg.SGG

WHERE d.SGG IN ('서초구', '영등포구', '중구');


-- ========================================
-- Step 2: DONG_FEAT_DK_PRICE — DataKnows AI 시세 피처
-- T/F 축 보강: dk_avg_price_pyeong (AI 추정 매매 평당가)
-- J/P 축 보강: dk_price_cv (AI 시세 변동계수, 높을수록 P)
-- 데이터 기간: 2012-01 ~ 2026-03 (기존 RICHGO 2025Q2보다 최신)
-- ========================================
CREATE OR REPLACE TABLE DONG_FEAT_DK_PRICE AS
WITH
-- EMD 레벨 AI 시세 (정확 매칭용)
price_emd_exact AS (
    SELECT
        SGG,
        EMD,
        ROUND(AVG(MEAN_MEME_PRICE), 0)                                          AS dk_avg_price,
        ROUND(AVG(MEME_PRICE_PER_SUPPLY_PYEONG), 0)                             AS dk_avg_price_pyeong,
        ROUND(AVG(MEAN_JEONSE_PRICE), 0)                                        AS dk_avg_jeonse,
        ROUND(
            STDDEV(MEME_PRICE_PER_SUPPLY_PYEONG) /
            NULLIF(AVG(MEME_PRICE_PER_SUPPLY_PYEONG), 0)
        , 4)                                                                     AS dk_price_cv,
        -- 전세/매매 비율 (낮을수록 고급 매매 시장 = T 방향 강화)
        ROUND(
            AVG(MEAN_JEONSE_PRICE) / NULLIF(AVG(MEAN_MEME_PRICE), 0)
        , 4)                                                                     AS dk_jeonse_ratio
    FROM KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE
         .HACKATHON_2026.REGION_APT_RICHGO_MARKET_PRICE_M_H
    WHERE REGION_LEVEL = 'emd'
      AND SD = '서울'
      AND SGG IN ('서초구', '영등포구', '중구')
      AND MEME_PRICE_PER_SUPPLY_PYEONG > 0
    GROUP BY SGG, EMD
),
-- EMD 레벨 AI 시세 (퍼지 매칭용 — 같은 데이터, 조인 키만 다름)
price_emd_fuzzy AS (
    SELECT
        SGG,
        EMD                                                                      AS emd_src,
        ROUND(AVG(MEAN_MEME_PRICE), 0)                                          AS dk_avg_price,
        ROUND(AVG(MEME_PRICE_PER_SUPPLY_PYEONG), 0)                             AS dk_avg_price_pyeong,
        ROUND(AVG(MEAN_JEONSE_PRICE), 0)                                        AS dk_avg_jeonse,
        ROUND(
            STDDEV(MEME_PRICE_PER_SUPPLY_PYEONG) /
            NULLIF(AVG(MEME_PRICE_PER_SUPPLY_PYEONG), 0)
        , 4)                                                                     AS dk_price_cv,
        ROUND(
            AVG(MEAN_JEONSE_PRICE) / NULLIF(AVG(MEAN_MEME_PRICE), 0)
        , 4)                                                                     AS dk_jeonse_ratio
    FROM KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE
         .HACKATHON_2026.REGION_APT_RICHGO_MARKET_PRICE_M_H
    WHERE REGION_LEVEL = 'emd'
      AND SD = '서울'
      AND SGG IN ('서초구', '영등포구', '중구')
      AND MEME_PRICE_PER_SUPPLY_PYEONG > 0
    GROUP BY SGG, EMD
),
-- SGG 레벨 폴백
price_sgg AS (
    SELECT
        SGG,
        ROUND(AVG(MEAN_MEME_PRICE), 0)                                          AS dk_avg_price_sgg,
        ROUND(AVG(MEME_PRICE_PER_SUPPLY_PYEONG), 0)                             AS dk_avg_price_pyeong_sgg,
        ROUND(AVG(MEAN_JEONSE_PRICE), 0)                                        AS dk_avg_jeonse_sgg,
        ROUND(
            STDDEV(MEME_PRICE_PER_SUPPLY_PYEONG) /
            NULLIF(AVG(MEME_PRICE_PER_SUPPLY_PYEONG), 0)
        , 4)                                                                     AS dk_price_cv_sgg,
        ROUND(
            AVG(MEAN_JEONSE_PRICE) / NULLIF(AVG(MEAN_MEME_PRICE), 0)
        , 4)                                                                     AS dk_jeonse_ratio_sgg
    FROM KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE
         .HACKATHON_2026.REGION_APT_RICHGO_MARKET_PRICE_M_H
    WHERE REGION_LEVEL = 'sgg'
      AND SD = '서울'
      AND SGG IN ('서초구', '영등포구', '중구')
      AND MEME_PRICE_PER_SUPPLY_PYEONG > 0
    GROUP BY SGG
)
SELECT
    d.SGG,
    d.EMD,
    d.CITY_CODE,
    d.DISTRICT_CODE,

    -- AI 추정 매매가 (EMD 정확 → 퍼지 → SGG 폴백)
    COALESCE(pe.dk_avg_price,        pf.dk_avg_price,        ps.dk_avg_price_sgg)        AS dk_avg_price,
    COALESCE(pe.dk_avg_price_pyeong, pf.dk_avg_price_pyeong, ps.dk_avg_price_pyeong_sgg) AS dk_avg_price_pyeong,
    COALESCE(pe.dk_avg_jeonse,       pf.dk_avg_jeonse,       ps.dk_avg_jeonse_sgg)       AS dk_avg_jeonse,

    -- AI 시세 변동성 (J/P축 — 높을수록 P 방향)
    COALESCE(pe.dk_price_cv,         pf.dk_price_cv,         ps.dk_price_cv_sgg)         AS dk_price_cv,

    -- 전세/매매 비율 (낮을수록 고가 매매 시장)
    COALESCE(pe.dk_jeonse_ratio,     pf.dk_jeonse_ratio,     ps.dk_jeonse_ratio_sgg)     AS dk_jeonse_ratio,

    -- 데이터 출처 추적 (디버깅용)
    CASE
        WHEN pe.EMD IS NOT NULL THEN 'emd_exact'
        WHEN pf.emd_src IS NOT NULL THEN 'emd_fuzzy'
        ELSE 'sgg_fallback'
    END                                                                                   AS dk_price_source

FROM DONGNE_MBTI.PUBLIC.DONGNE_MASTER d

-- 1순위: 정확 매칭
LEFT JOIN price_emd_exact pe
    ON d.SGG = pe.SGG AND d.EMD = pe.EMD

-- 2순위: 퍼지 매칭 (당산동1가 → 당산동)
LEFT JOIN price_emd_fuzzy pf
    ON d.SGG = pf.SGG
    AND REGEXP_REPLACE(d.EMD, '[0-9]+가$', '') = pf.emd_src
    AND pe.EMD IS NULL   -- 정확 매칭 없을 때만

-- 3순위: SGG 폴백
LEFT JOIN price_sgg ps ON d.SGG = ps.SGG

WHERE d.SGG IN ('서초구', '영등포구', '중구');


-- ========================================
-- 검증 1: 테이블 행 수 + NULL 체크
-- ========================================
SELECT 'DONG_FEAT_SUBWAY' AS tbl,
    COUNT(*) AS total,
    COUNT(avg_subway_distance_m) AS has_distance,
    COUNT(avg_station_ridership) AS has_ridership,
    SUM(apt_danji_count) AS total_danji
FROM DONG_FEAT_SUBWAY
UNION ALL
SELECT 'DONG_FEAT_DK_PRICE',
    COUNT(*),
    COUNT(dk_avg_price),
    COUNT(dk_price_cv),
    NULL
FROM DONG_FEAT_DK_PRICE;
-- 기대: 각 118건, NULL 거의 없음 (SGG 폴백 작동)

-- ========================================
-- 검증 2: DataKnows 가격 데이터 소스 분포
-- ========================================
SELECT dk_price_source, SGG, COUNT(*) AS cnt
FROM DONG_FEAT_DK_PRICE
GROUP BY dk_price_source, SGG
ORDER BY dk_price_source, SGG;
-- 기대: 서초구 대부분 emd_exact, 영등포구 emd_fuzzy 증가, 중구 sgg_fallback 많음

-- ========================================
-- 검증 3: 구별 역세권 지표 (합리성 체크)
-- ========================================
SELECT
    SGG,
    ROUND(AVG(avg_subway_distance_m), 0)  AS avg_dist_m,
    ROUND(AVG(avg_station_ridership), 0)  AS avg_ridership,
    ROUND(AVG(subway_access_ratio), 2)    AS avg_access_ratio
FROM DONG_FEAT_SUBWAY
GROUP BY SGG
ORDER BY avg_dist_m;
-- 기대: 중구 < 영등포구 < 서초구 (중구가 중심가라 역세권 가장 가까움)

-- ========================================
-- 검증 4: 구별 AI 시세 (합리성 체크)
-- ========================================
SELECT
    SGG,
    ROUND(AVG(dk_avg_price_pyeong) / 10000, 1) AS avg_price_per_pyeong_eok,
    ROUND(AVG(dk_price_cv), 4) AS avg_price_volatility
FROM DONG_FEAT_DK_PRICE
GROUP BY SGG
ORDER BY avg_price_per_pyeong_eok DESC;
-- 기대: 서초구 > 영등포구 > 중구 (아파트 시세 순)
