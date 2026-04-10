-- =============================================================
-- 00_verify.sql
-- 배포 전·후 검증 쿼리 모음
-- 실행 전 비용 추정 + 배포 상태 확인
-- =============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;

-- ──────────────────────────────────────────────
-- 1. 사전 비용 추정 (AI_COUNT_TOKENS)
-- ──────────────────────────────────────────────

-- AI_COMPLETE 전체 실행 전: 토큰 수 사전 추정 (118건 × 2회 = CHARACTER_SUMMARY + PROFILE_TEXT)
-- 실행 비용 = 토큰 수 × 모델 단가 (mistral-7b: $0.00006/1K tokens, large2: $0.003/1K)
SELECT
    COUNT(*) AS row_count,
    ROUND(AVG(SNOWFLAKE.CORTEX.COUNT_TOKENS(
        'snowflake-arctic',
        '서울 ' || SGG || ' ' || EMD || '동의 MBTI는 ' || MBTI || '입니다. 한 문장(30자 이내)으로 표현해주세요.'
    )), 1) AS avg_tokens_per_row,
    ROUND(SUM(SNOWFLAKE.CORTEX.COUNT_TOKENS(
        'snowflake-arctic',
        '서울 ' || SGG || ' ' || EMD || '동의 MBTI는 ' || MBTI || '입니다. 한 문장(30자 이내)으로 표현해주세요.'
    )), 1) AS total_tokens_estimate,
    -- arctic 단가: $0.003 / 1K tokens
    ROUND(SUM(SNOWFLAKE.CORTEX.COUNT_TOKENS(
        'snowflake-arctic',
        '서울 ' || SGG || ' ' || EMD || '동의 MBTI는 ' || MBTI || '입니다. 한 문장(30자 이내)으로 표현해주세요.'
    )) / 1000 * 0.003, 4) AS estimated_cost_usd
FROM DONGNE_MBTI.PUBLIC.DONG_MBTI_RESULT;
-- 기대: 118건 × ~50 tokens ≈ 6K tokens ≈ $0.02

-- ──────────────────────────────────────────────
-- 2. 배포 상태 확인
-- ──────────────────────────────────────────────

-- SiS 배포 확인
SHOW STREAMLITS IN SCHEMA DONGNE_MBTI.PUBLIC;

-- Cortex Search 서비스 확인
SHOW CORTEX SEARCH SERVICES LIKE 'DONGNE_SEARCH' IN SCHEMA DONGNE_MBTI.PUBLIC;

-- Cortex Agent 확인 (DDL 존재 여부)
SHOW AGENTS LIKE 'DONGNE_AGENT' IN SCHEMA DONGNE_MBTI.PUBLIC;

-- ──────────────────────────────────────────────
-- 3. 데이터 품질 확인
-- ──────────────────────────────────────────────

-- DONG_PROFILES 컬럼 채움 상태
SELECT
    COUNT(*) AS total,
    COUNT(CHARACTER_SUMMARY) AS has_summary,
    COUNT(PROFILE_TEXT) AS has_profile,
    COUNT(NEIGHBORHOOD_TYPE) AS has_classify,
    COUNT(SENTIMENT_SCORE) AS has_sentiment,
    COUNT(DISTINCT MBTI) AS mbti_types
FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES;
-- 기대: total=118, 모든 컬럼 채워짐, mbti_types=16

-- ML FORECAST 결과 확인
SELECT COUNT(DISTINCT SERIES) AS series_count, COUNT(*) AS forecast_rows
FROM DONGNE_MBTI.PUBLIC.PRICE_FORECAST_RESULT;
-- 기대: series_count = 동 수 (최대 118), forecast_rows = series × 3

-- ──────────────────────────────────────────────
-- 4. 크레딧 소비 현황 (일일 확인용)
-- ──────────────────────────────────────────────
SELECT
    DATE_TRUNC('day', START_TIME) AS usage_date,
    ROUND(SUM(CREDITS_USED), 3) AS credits_used
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY usage_date
ORDER BY usage_date DESC;
