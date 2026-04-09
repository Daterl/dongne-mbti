/*==========================================================
  08_streamlit_deploy.sql
  Streamlit in Snowflake (SiS) 앱 배포
  (이슈 #17: 동네 MBTI 대시보드)
==========================================================*/

USE SCHEMA DONGNE_MBTI.PUBLIC;

--------------------------------------------------------------
-- 1) Git Repository 최신 동기화
--------------------------------------------------------------
ALTER GIT REPOSITORY dongne_repo FETCH;

--------------------------------------------------------------
-- 2) Streamlit 앱 생성 (Git repo 기반)
--------------------------------------------------------------
CREATE OR REPLACE STREAMLIT DONGNE_MBTI_APP
    ROOT_LOCATION = '@DONGNE_MBTI.PUBLIC.dongne_repo/branches/main/streamlit'
    MAIN_FILE = 'app.py'
    QUERY_WAREHOUSE = 'COMPUTE_WH';

--------------------------------------------------------------
-- 3) 앱 확인
--------------------------------------------------------------
SHOW STREAMLITS LIKE 'DONGNE_MBTI_APP' IN SCHEMA DONGNE_MBTI.PUBLIC;
