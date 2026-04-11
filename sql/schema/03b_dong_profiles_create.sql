-- =============================================================
-- 03b_dong_profiles_create.sql
-- DONG_PROFILES 테이블 생성 + AI_COMPLETE로 프로필 텍스트 생성
-- 이슈 #9: AI_COMPLETE 활용 동네 성격 프로필 생성
-- =============================================================
-- 의존: DONG_MBTI_RESULT, DONG_FEAT_TF, DONG_FEAT_JP
-- 크레딧: ~$2-3 (AI_COMPLETE 118건 × 2회 호출)
-- ⚠️ 반드시 03_dong_mbti_result.sql 실행 후 실행
-- =============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;

-- ========================================
-- Step 1: DONG_PROFILES 기본 테이블 생성
-- DONG_MBTI_RESULT + 피처 데이터 결합
-- ========================================
CREATE OR REPLACE TABLE DONG_PROFILES AS
SELECT
    r.SGG,
    r.EMD,
    r.CITY_CODE,
    r.DISTRICT_CODE,
    r.MBTI,
    r.EI_SCORE,
    r.SN_SCORE,
    r.TF_SCORE,
    r.JP_SCORE,
    r.EI_STRENGTH,
    r.SN_STRENGTH,
    r.TF_STRENGTH,
    r.JP_STRENGTH,
    -- 피처 원본 (앱 상세 표시용)
    tf.AVG_INCOME,
    tf.AVG_ASSET,
    tf.AVG_PRICE,
    jp.YOUNG_RATIO,
    jp.PRICE_CV,
    -- DataKnows AI 시세
    dk.DK_AVG_PRICE_PYEONG,
    dk.DK_PRICE_CV,
    -- 역세권
    sb.AVG_SUBWAY_DISTANCE_M,
    sb.AVG_STATION_RIDERSHIP,
    sb.SUBWAY_ACCESS_RATIO,
    -- AI 생성 텍스트 (Step 2에서 채움)
    NULL::VARCHAR(500)  AS CHARACTER_SUMMARY,
    NULL::VARCHAR(2000) AS PROFILE_TEXT,
    -- 04·05에서 채울 컬럼
    NULL::VARCHAR(100)  AS NEIGHBORHOOD_TYPE,
    NULL::FLOAT         AS SENTIMENT_SCORE
FROM DONG_MBTI_RESULT r
LEFT JOIN DONG_FEAT_TF tf ON r.DISTRICT_CODE = tf.DISTRICT_CODE
LEFT JOIN DONG_FEAT_JP jp ON r.DISTRICT_CODE = jp.DISTRICT_CODE
LEFT JOIN DONG_FEAT_DK_PRICE dk ON r.DISTRICT_CODE = dk.DISTRICT_CODE
LEFT JOIN DONG_FEAT_SUBWAY sb ON r.DISTRICT_CODE = sb.DISTRICT_CODE;

-- 검증: 118건 확인
SELECT COUNT(*) AS total, COUNT(DISTINCT MBTI) AS mbti_types
FROM DONG_PROFILES;


-- ========================================
-- Step 2: CHARACTER_SUMMARY 생성 (AI_COMPLETE)
-- 한 줄 성격 요약 (Cortex Search ATTRIBUTES용)
-- ========================================
-- AISQL 신함수 AI_COMPLETE + Llama 3.3 70B (최신 오픈 모델, 'auto' 셀렉터 미지원 리전)
UPDATE DONG_PROFILES
SET CHARACTER_SUMMARY = AI_COMPLETE(
    'llama3.3-70b',
    '서울 ' || SGG || ' ' || EMD || '동의 MBTI는 ' || MBTI || '입니다. ' ||
    '다음 특성을 가진 이 동네를 한 문장(30자 이내)으로 매력적으로 표현해주세요: ' ||
    CASE WHEN EI_SCORE > 0 THEN '활기찬 유동인구' ELSE '조용한 주거 분위기' END || ', ' ||
    CASE WHEN SN_SCORE > 0 THEN '생활밀착형 소비' ELSE '문화·교육 중심 소비' END || ', ' ||
    CASE WHEN TF_SCORE > 0 THEN '고소득·고자산 지역' ELSE '서민적 감성 동네' END || ', ' ||
    CASE WHEN JP_SCORE > 0 THEN '안정적 정착 동네' ELSE '역동적 변화 동네' END ||
    '. 동네 이름과 MBTI를 언급하지 말고 성격만 표현해주세요.'
);

-- ========================================
-- Step 3: PROFILE_TEXT 생성 (AI_COMPLETE)
-- 상세 동네 프로필 (Cortex Agent search_dongne 검색 대상)
-- ========================================
-- AISQL 신함수 AI_COMPLETE + Llama 3.3 70B (최신 오픈 모델, 'auto' 셀렉터 미지원 리전)
UPDATE DONG_PROFILES
SET PROFILE_TEXT = AI_COMPLETE(
    'llama3.3-70b',
    '서울 ' || SGG || ' ' || EMD || '의 동네 MBTI 성격 프로필을 작성해주세요. ' ||
    'MBTI 유형: ' || MBTI || '\n' ||
    '4축 점수:\n' ||
    '- E/I: ' || ROUND(EI_SCORE, 2) || ' (' || CASE WHEN EI_SCORE > 0 THEN 'E-외향' ELSE 'I-내향' END || ')\n' ||
    '- S/N: ' || ROUND(SN_SCORE, 2) || ' (' || CASE WHEN SN_SCORE > 0 THEN 'S-현실' ELSE 'N-직관' END || ')\n' ||
    '- T/F: ' || ROUND(TF_SCORE, 2) || ' (' || CASE WHEN TF_SCORE > 0 THEN 'T-이성' ELSE 'F-감성' END || ')\n' ||
    '- J/P: ' || ROUND(JP_SCORE, 2) || ' (' || CASE WHEN JP_SCORE > 0 THEN 'J-안정' ELSE 'P-탐색' END || ')\n' ||
    '200자 내외로 이 동네의 성격, 분위기, 어울리는 사람을 친근하고 재미있게 설명해주세요.'
);

-- ========================================
-- 검증: AI 텍스트 생성 확인
-- ========================================
SELECT SGG, EMD, MBTI,
    LEFT(CHARACTER_SUMMARY, 50) AS summary_preview,
    LENGTH(PROFILE_TEXT) AS profile_len
FROM DONG_PROFILES
ORDER BY SGG, EMD
LIMIT 5;

SELECT
    COUNT(*) AS total,
    COUNT(CHARACTER_SUMMARY) AS has_summary,
    COUNT(PROFILE_TEXT) AS has_profile,
    ROUND(AVG(LENGTH(PROFILE_TEXT))) AS avg_profile_len
FROM DONG_PROFILES;
-- 기대: 118건 전부 summary·profile 있음
