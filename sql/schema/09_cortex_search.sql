-- =============================================================
-- 09_cortex_search.sql
-- 이슈 #11: Cortex Search Service 생성 (Agent search_dongne 도구 대상)
-- =============================================================
-- DONG_PROFILES.PROFILE_TEXT를 하이브리드(벡터+키워드) 검색 인덱싱
-- TARGET_LAG='1 day' → 증분 인덱싱 (primary key 기반, 비용 50-70% 절감)
-- =============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;

CREATE OR REPLACE CORTEX SEARCH SERVICE DONGNE_MBTI.PUBLIC.DONGNE_SEARCH
  ON PROFILE_TEXT
  ATTRIBUTES SGG, EMD, MBTI, CHARACTER_SUMMARY
  WAREHOUSE = COMPUTE_WH
  TARGET_LAG = '1 day'
  AS
    SELECT
        SGG,
        EMD,
        MBTI,
        CHARACTER_SUMMARY,
        PROFILE_TEXT
    FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES
    WHERE PROFILE_TEXT IS NOT NULL;

-- 검증
SHOW CORTEX SEARCH SERVICES LIKE 'DONGNE_SEARCH' IN SCHEMA DONGNE_MBTI.PUBLIC;
DESCRIBE CORTEX SEARCH SERVICE DONGNE_MBTI.PUBLIC.DONGNE_SEARCH;
