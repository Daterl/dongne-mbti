-- =============================================================
-- 11_dynamic_table_profiles.sql
-- Dynamic Table: DONG_PROFILES_ENRICHED
-- =============================================================
-- 왜 Dynamic Table인가 (3줄 요약):
--   1) 선언적 파이프라인 — Cortex 감성 분석을 SELECT 절 내부에 내장해
--      "데이터 신선도 SLA" (TARGET_LAG)를 Snowflake 스케줄러에게 위임
--   2) 기존 05_dong_profiles_sentiment.sql 배치 UPDATE 경로와
--      **동일 함수 (SNOWFLAKE.CORTEX.SENTIMENT, FLOAT 반환)**로 공존
--      → 두 결과를 1:1 비교 가능 (배치 vs. 증분 재계산)
--   3) 앱 (streamlit/app.py)은 변경하지 않음 — 이 테이블은 증거 레이어로만 기능
-- =============================================================
-- 의존: DONG_PROFILES (03b·04·05 실행 완료 상태)
-- 크레딧 주의: CREATE OR REPLACE 시점에 TARGET_LAG과 무관하게
--              전체 초기 refresh가 1회 실행됨. 실행 전 사전 측정 필수.
-- =============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;

-- ========================================
-- Step 0: 초기 refresh 비용 사전 측정 (LIMIT 10)
-- 반드시 CREATE 전에 실행. 예상 비용 $0.5 초과 시 재검토.
-- ========================================
-- SELECT SNOWFLAKE.CORTEX.SENTIMENT(PROFILE_TEXT) AS sentiment_preview
-- FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES
-- WHERE PROFILE_TEXT IS NOT NULL
-- LIMIT 10;

-- ========================================
-- Step 1: Dynamic Table 생성
-- ========================================
CREATE OR REPLACE DYNAMIC TABLE DONGNE_MBTI.PUBLIC.DONG_PROFILES_ENRICHED
  TARGET_LAG = '1 day'
  WAREHOUSE = COMPUTE_WH
  AS
    SELECT
        SGG,
        EMD,
        CITY_CODE,
        DISTRICT_CODE,
        MBTI,
        EI_SCORE,
        SN_SCORE,
        TF_SCORE,
        JP_SCORE,
        CHARACTER_SUMMARY,
        PROFILE_TEXT,
        NEIGHBORHOOD_TYPE,
        SENTIMENT_SCORE AS sentiment_score_batch,
        -- 공존 포인트: 배치 UPDATE(05)와 동일한 legacy 함수 사용
        -- → sentiment_score_batch 와 sentiment_score_dynamic 가 동일 값이어야 정상
        SNOWFLAKE.CORTEX.SENTIMENT(PROFILE_TEXT) AS sentiment_score_dynamic
    FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES
    WHERE PROFILE_TEXT IS NOT NULL;

-- ========================================
-- Step 2: 생성 직후 즉시 warehouse suspend (비용 가드)
-- ========================================
ALTER WAREHOUSE COMPUTE_WH SUSPEND;

-- ========================================
-- Step 3: 검증
-- ========================================
-- Dynamic Table 상태
SHOW DYNAMIC TABLES LIKE 'DONG_PROFILES_ENRICHED' IN SCHEMA DONGNE_MBTI.PUBLIC;

-- Row count 일치성 (DONG_PROFILES와 동일해야 함)
SELECT
    (SELECT COUNT(*) FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES WHERE PROFILE_TEXT IS NOT NULL) AS source_rows,
    (SELECT COUNT(*) FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES_ENRICHED)                      AS enriched_rows;

-- 스키마 공존 검증: 배치 결과와 동적 결과가 동일 함수이므로 값이 같아야 함
SELECT
    SGG,
    EMD,
    ROUND(sentiment_score_batch, 4)   AS batch_score,
    ROUND(sentiment_score_dynamic, 4) AS dynamic_score,
    ROUND(ABS(sentiment_score_batch - sentiment_score_dynamic), 4) AS delta
FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES_ENRICHED
ORDER BY delta DESC
LIMIT 5;
-- 기대: delta = 0 (완전 일치) — 동일 함수·동일 입력이므로

-- 집계 검증
SELECT
    COUNT(*)                                  AS total,
    COUNT(DISTINCT MBTI)                      AS mbti_types,
    ROUND(AVG(sentiment_score_dynamic), 4)    AS avg_sentiment
FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES_ENRICHED;
