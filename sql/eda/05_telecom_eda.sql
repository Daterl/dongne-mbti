-- ============================================================
-- 05. 아정당(AJD) 텔레콤 데이터 EDA
-- 목표: 컬럼 확인 + 서울 25구 커버리지 검증 + MBTI 피처 후보 탐색
-- ============================================================
-- [미채택 결정 — 2026-04-08]
-- 텔레콤 데이터(V01·V05)는 구(區) 단위만 제공하여
-- 동(洞) 단위 분석(3구 55개 동)에 JOIN이 불가함.
-- → 최종 파이프라인(sql/schema/)에서 제외. 이 파일은 탐색 기록으로만 보존.
-- ============================================================

-- ========================================
-- A. V01: 월별 지역별 계약 통계
-- ========================================

-- A-1: 컬럼 확인
SELECT * FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
    .TELECOM_INSIGHTS.V01_MONTHLY_REGIONAL_CONTRACT_STATS
LIMIT 5;

-- A-2: 서울 지역 필터링 + 구 목록
SELECT DISTINCT INSTALL_CITY
FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
    .TELECOM_INSIGHTS.V01_MONTHLY_REGIONAL_CONTRACT_STATS
WHERE INSTALL_STATE = '서울'
ORDER BY INSTALL_CITY;

-- ========================================
-- B. V05: 지역별 신규 설치
-- ========================================

-- B-1: 컬럼 확인
SELECT * FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
    .TELECOM_INSIGHTS.V05_REGIONAL_NEW_INSTALL
LIMIT 5;

-- B-2: 서울 구별 신규설치 건수
SELECT INSTALL_CITY, COUNT(*) AS cnt
FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
    .TELECOM_INSIGHTS.V05_REGIONAL_NEW_INSTALL
WHERE INSTALL_STATE = '서울'
GROUP BY INSTALL_CITY
ORDER BY INSTALL_CITY;

-- ========================================
-- C. V02: 서비스 번들 패턴
-- ========================================

-- C-1: 컬럼 확인
SELECT * FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
    .TELECOM_INSIGHTS.V02_SERVICE_BUNDLE_PATTERNS
LIMIT 5;

-- ========================================
-- D. V09: 월별 상담 통계
-- ========================================

-- D-1: 컬럼 확인
SELECT * FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
    .TELECOM_INSIGHTS.V09_MONTHLY_CALL_STATS
LIMIT 5;

-- ========================================
-- E. V03: 계약 전환율 퍼널
-- ========================================

-- E-1: 컬럼 확인
SELECT * FROM SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__INSTALL_SUBSCRIPTION_MARKETING_CHANNEL_FUNNEL_ANALYSIS
    .TELECOM_INSIGHTS.V03_CONTRACT_FUNNEL_CONVERSION
LIMIT 5;
