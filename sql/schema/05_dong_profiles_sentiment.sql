-- =============================================================
-- 05_dong_profiles_sentiment.sql
-- 이슈 #8: AI_SENTIMENT로 PROFILE_TEXT 감성 점수 추가
-- =============================================================
-- 병렬 경로 (선언적 파이프라인): sql/schema/11_dynamic_table_profiles.sql
-- → Dynamic Table DONG_PROFILES_ENRICHED 가 동일한 SNOWFLAKE.CORTEX.SENTIMENT
--   함수를 SELECT 절 내부에 내장하여 배치 UPDATE 경로와 의도적으로 공존함.
-- =============================================================

-- DONG_PROFILES에 SENTIMENT_SCORE 컬럼 추가
ALTER TABLE DONGNE_MBTI.PUBLIC.DONG_PROFILES
  ADD COLUMN IF NOT EXISTS SENTIMENT_SCORE FLOAT;

-- AI_SENTIMENT로 PROFILE_TEXT 감성 분석
UPDATE DONGNE_MBTI.PUBLIC.DONG_PROFILES
SET SENTIMENT_SCORE = SNOWFLAKE.CORTEX.SENTIMENT(PROFILE_TEXT);

-- 검증
SELECT
    COUNT(*) AS total,
    ROUND(MIN(SENTIMENT_SCORE), 4) AS min_score,
    ROUND(AVG(SENTIMENT_SCORE), 4) AS avg_score,
    ROUND(MAX(SENTIMENT_SCORE), 4) AS max_score,
    SUM(CASE WHEN SENTIMENT_SCORE > 0.1 THEN 1 ELSE 0 END) AS positive,
    SUM(CASE WHEN SENTIMENT_SCORE BETWEEN -0.1 AND 0.1 THEN 1 ELSE 0 END) AS neutral,
    SUM(CASE WHEN SENTIMENT_SCORE < -0.1 THEN 1 ELSE 0 END) AS negative
FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES;
