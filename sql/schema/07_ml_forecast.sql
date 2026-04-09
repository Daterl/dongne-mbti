/*==========================================================
  07_ml_forecast.sql
  ML FORECAST — 동별 아파트 매매 평당가 3개월 예측
  (이슈 #16: 탭3 이사 예보)
==========================================================*/

USE SCHEMA DONGNE_MBTI.PUBLIC;

--------------------------------------------------------------
-- 1) 훈련 데이터 뷰: 서울 3구 동별 월평균 매매 평당가
--------------------------------------------------------------
CREATE OR REPLACE VIEW PRICE_TIMESERIES AS
SELECT
    SGG || '_' || EMD          AS SERIES,
    YYYYMMDD::TIMESTAMP_NTZ    AS TS,
    AVG(MEME_PRICE_PER_SUPPLY_PYEONG) AS AVG_PRICE
FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
    .HACKATHON_2025Q2.REGION_APT_RICHGO_MARKET_PRICE_M_H
WHERE SD = '서울'
  AND SGG IN ('서초구', '영등포구', '중구')
  AND MEME_PRICE_PER_SUPPLY_PYEONG > 0
GROUP BY SERIES, TS;

--------------------------------------------------------------
-- 2) ML FORECAST 모델 생성 (다중 시계열, XSMALL WH)
--------------------------------------------------------------
CREATE OR REPLACE SNOWFLAKE.ML.FORECAST PRICE_FORECAST(
    INPUT_DATA      => SYSTEM$REFERENCE('VIEW', 'DONGNE_MBTI.PUBLIC.PRICE_TIMESERIES'),
    SERIES_COLNAME  => 'SERIES',
    TIMESTAMP_COLNAME => 'TS',
    TARGET_COLNAME  => 'AVG_PRICE',
    CONFIG_OBJECT   => {'ON_ERROR': 'SKIP'}
);

--------------------------------------------------------------
-- 3) 향후 3개월 예측 결과 저장 (90% 신뢰구간)
--------------------------------------------------------------
CREATE OR REPLACE TABLE PRICE_FORECAST_RESULT AS
SELECT * FROM TABLE(
    PRICE_FORECAST!FORECAST(
        FORECASTING_PERIODS => 3,
        CONFIG_OBJECT => {'prediction_interval': 0.9}
    )
);

--------------------------------------------------------------
-- 4) 검증 쿼리
--------------------------------------------------------------
SELECT SERIES, TS, ROUND(FORECAST, 1) AS FORECAST,
       ROUND(LOWER_BOUND, 1) AS LOWER_90,
       ROUND(UPPER_BOUND, 1) AS UPPER_90
FROM PRICE_FORECAST_RESULT
ORDER BY SERIES, TS;
