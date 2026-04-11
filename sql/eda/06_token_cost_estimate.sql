-- =============================================================
-- 06_token_cost_estimate.sql
-- 이슈 #R2: SNOWFLAKE.CORTEX.COUNT_TOKENS 기반 Tab2 호출 비용 사전 추정
-- =============================================================
-- 목적: Tab2 자연어 질의 1건당 평균 토큰·비용 추정으로
--       "설계 차원의 비용 가드레일" 심사 루브릭(R2) 충족
-- 실행 시점: 배포 전 1회 (EDA — 반복 실행 불필요)
-- 참고: AI_COUNT_TOKENS(AISQL 신함수)는 이 계정/리전 미지원
--       → SNOWFLAKE.CORTEX.COUNT_TOKENS(레거시 동등 함수) 사용
-- =============================================================

USE SCHEMA DONGNE_MBTI.PUBLIC;

-- ========================================
-- Step 1: 모델별 토큰 단가 기준 (2026-04 기준)
-- llama3.3-70b: 입력 $0.60/1M, 출력 $0.90/1M (Snowflake Cortex 공개 요금표)
-- ========================================

-- ========================================
-- Step 2: 대표 샘플 프롬프트 토큰 수 측정
--         Tab2 실제 호출 패턴을 반영한 멀티턴 1회 기준
-- ========================================
SELECT
    SNOWFLAKE.CORTEX.COUNT_TOKENS(
        'llama3.3-70b',
        '당신은 서울 동네 전문가입니다. 다음 동네 프로필을 참고하여 질문에 답하세요.\n\n[프로필 예시]\n서초구 반포동 — INTJ형 동네. 고요하고 계획적인 분위기.\n\n[질문]\n조용하고 학군 좋은 동네를 추천해줘.'
    ) AS sample_token_count,
    -- 입력 비용 추정 (llama3.3-70b 기준 $0.60/1M tokens)
    ROUND(
        SNOWFLAKE.CORTEX.COUNT_TOKENS(
            'llama3.3-70b',
            '당신은 서울 동네 전문가입니다. 다음 동네 프로필을 참고하여 질문에 답하세요.\n\n[프로필 예시]\n서초구 반포동 — INTJ형 동네. 고요하고 계획적인 분위기.\n\n[질문]\n조용하고 학군 좋은 동네를 추천해줘.'
        ) * 0.60 / 1000000,
        8
    ) AS estimated_input_cost_usd,
    -- 월 1,000회 호출 시 입력 비용 추정
    ROUND(
        SNOWFLAKE.CORTEX.COUNT_TOKENS(
            'llama3.3-70b',
            '당신은 서울 동네 전문가입니다. 다음 동네 프로필을 참고하여 질문에 답하세요.\n\n[프로필 예시]\n서초구 반포동 — INTJ형 동네. 고요하고 계획적인 분위기.\n\n[질문]\n조용하고 학군 좋은 동네를 추천해줘.'
        ) * 0.60 / 1000000 * 1000,
        4
    ) AS monthly_1k_calls_input_cost_usd;

-- ========================================
-- Step 3: 현재 배포된 DONG_PROFILES 텍스트 평균 토큰 수
--         (실제 Tab2 컨텍스트 주입 시 토큰 규모 파악)
-- ========================================
SELECT
    COUNT(*)                                AS total_rows,
    ROUND(AVG(
        SNOWFLAKE.CORTEX.COUNT_TOKENS('llama3.3-70b', PROFILE_TEXT)
    ), 0)                                   AS avg_profile_tokens,
    MAX(SNOWFLAKE.CORTEX.COUNT_TOKENS('llama3.3-70b', PROFILE_TEXT)) AS max_profile_tokens,
    -- 평균 프로필 1건 + 시스템 프롬프트(~200 tokens) 합산 비용
    ROUND(AVG(
        SNOWFLAKE.CORTEX.COUNT_TOKENS('llama3.3-70b', PROFILE_TEXT)
    ) * 0.60 / 1000000, 8)                 AS avg_cost_per_call_usd
FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES
WHERE PROFILE_TEXT IS NOT NULL;
