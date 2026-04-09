-- =============================================================
-- 04_dong_profiles_classify.sql
-- 이슈 #7: AI_CLASSIFY로 동네 성향 분류 (NEIGHBORHOOD_TYPE)
-- =============================================================

-- DONG_PROFILES에 NEIGHBORHOOD_TYPE 컬럼 추가
ALTER TABLE DONGNE_MBTI.PUBLIC.DONG_PROFILES
  ADD COLUMN IF NOT EXISTS NEIGHBORHOOD_TYPE VARCHAR(100);

-- AI_CLASSIFY_TEXT로 4축 점수 기반 동네 유형 분류
UPDATE DONGNE_MBTI.PUBLIC.DONG_PROFILES
SET NEIGHBORHOOD_TYPE = PARSE_JSON(
    SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
        '동네 특성: ' ||
        CASE WHEN EI_SCORE > 0 THEN '외향적(유동인구 많고 주말 활력 높음)' ELSE '내향적(조용하고 유동인구 적음)' END || ', ' ||
        CASE WHEN SN_SCORE > 0 THEN '현실적(생활밀착 소비 중심)' ELSE '직관적(교육·문화 소비 중심)' END || ', ' ||
        CASE WHEN TF_SCORE > 0 THEN '이성적(고소득·고자산·높은 시세)' ELSE '감성적(소규모·감성 소비 중심)' END || ', ' ||
        CASE WHEN JP_SCORE > 0 THEN '계획적(안정적 시세·고령 비율 높음)' ELSE '탐색적(변동성 크고 청년 비율 높음)' END,
        ARRAY_CONSTRUCT(
            '조용한 주거지',
            '상업/업무 중심',
            '젊은 문화 동네',
            '고급 주거지',
            '전통 상업지구',
            '교육/문화 중심'
        )
    )
):label::VARCHAR;

-- 검증
SELECT NEIGHBORHOOD_TYPE, COUNT(*) AS cnt
FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES
GROUP BY NEIGHBORHOOD_TYPE
ORDER BY cnt DESC;
