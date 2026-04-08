-- ============================================================
-- 01. DONGNE_MASTER — 동네 마스터 테이블
-- 서울 전체 동 목록 + 구 매핑 + 리치고 JOIN 키
-- 의존: SPH M_SCCO_MST
-- ============================================================

-- 스키마/DB 설정
USE ROLE ACCOUNTADMIN;
CREATE DATABASE IF NOT EXISTS DONGNE_MBTI;
CREATE SCHEMA IF NOT EXISTS DONGNE_MBTI.PUBLIC;
USE SCHEMA DONGNE_MBTI.PUBLIC;

-- DONGNE_MASTER: 서울 전체 동 목록 (JOIN 허브)
CREATE OR REPLACE TABLE DONGNE_MASTER AS
SELECT
    m.PROVINCE_CODE,
    m.CITY_CODE,                          -- 구 코드 (SPH JOIN 키)
    m.DISTRICT_CODE,                      -- 동 코드 (SPH JOIN 키)
    m.PROVINCE_KOR_NAME AS SD_FULL,       -- '서울특별시'
    '서울' AS SD,                          -- 리치고 JOIN 키
    m.CITY_KOR_NAME AS SGG,              -- 구 이름 (리치고 JOIN 키)
    m.DISTRICT_KOR_NAME AS EMD,          -- 동 이름 (리치고 JOIN 키)
    m.CITY_ENG_NAME AS SGG_EN,           -- 구 영문명
    m.DISTRICT_ENG_NAME AS EMD_EN,       -- 동 영문명
    m.DISTRICT_GEOM                       -- 지리 공간 데이터
FROM SEOUL_DISTRICTLEVEL_DATA_FLOATING_POPULATION_CONSUMPTION_AND_ASSETS
    .GRANDATA.M_SCCO_MST m
WHERE m.PROVINCE_KOR_NAME = '서울특별시';

-- 검증
SELECT COUNT(*) AS total_dong, COUNT(DISTINCT SGG) AS gu_count
FROM DONGNE_MASTER;
-- 기대: ~467동, 25구

-- 구별 동 수 확인
SELECT SGG, COUNT(*) AS dong_count
FROM DONGNE_MASTER
GROUP BY SGG
ORDER BY SGG;
