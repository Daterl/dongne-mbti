/*==========================================================
  08b_streamlit_deploy_dev.sql
  Dev 버전 Streamlit 앱 배포 (dev 브랜치 기반)
  - main의 DONGNE_MBTI_APP은 건드리지 않음
  - dev 브랜치의 코드로 별도 앱 생성
==========================================================*/

USE SCHEMA DONGNE_MBTI.PUBLIC;

--------------------------------------------------------------
-- 1) Git Repository 최신 동기화
--------------------------------------------------------------
ALTER GIT REPOSITORY dongne_repo FETCH;

--------------------------------------------------------------
-- 2) Dev Streamlit 앱 생성 (dev 브랜치 기반)
--------------------------------------------------------------
CREATE OR REPLACE STREAMLIT DONGNE_MBTI_DEV
    ROOT_LOCATION = '@DONGNE_MBTI.PUBLIC.dongne_repo/branches/dev/streamlit'
    MAIN_FILE = 'app.py'
    QUERY_WAREHOUSE = 'COMPUTE_WH';

--------------------------------------------------------------
-- 3) 앱 확인
--------------------------------------------------------------
SHOW STREAMLITS LIKE 'DONGNE_MBTI%' IN SCHEMA DONGNE_MBTI.PUBLIC;
