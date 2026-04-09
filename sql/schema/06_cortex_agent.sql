-- =============================================================
-- 06_cortex_agent.sql
-- 이슈 #12: Cortex Agent 생성 (Search + Analyst 조합)
-- =============================================================

-- Cortex Agent: dongne_search(Search) + dongne_mbti.yaml(Analyst) 통합
CREATE OR REPLACE AGENT DONGNE_MBTI.PUBLIC.DONGNE_AGENT
FROM SPECIFICATION $$
{
  "models": {
    "orchestration": "auto"
  },
  "orchestration": {
    "budget": {
      "seconds": 300,
      "tokens": 200000
    }
  },
  "instructions": {
    "orchestration": "당신은 서울 3구(서초구, 영등포구, 중구) 118개 동네의 MBTI 성격 분석 전문가입니다. 사용자가 동네를 추천해달라고 하면 search_dongne 도구로 관련 동네 프로필을 검색하세요. 수치 데이터(점수, 시세, 소득 등)를 물어보면 query_dongne 도구로 SQL 쿼리를 실행하세요. 두 도구를 조합해서 풍부한 답변을 제공하세요.",
    "response": "한국어로 답변하세요. 동네 이름과 MBTI 유형을 항상 포함하세요. 수치 데이터가 있으면 구체적인 숫자를 제시하세요. 친근하고 재미있는 톤으로 동네 성격을 설명하세요."
  },
  "tools": [
    {
      "tool_spec": {
        "type": "cortex_search",
        "name": "search_dongne",
        "description": "서울 3구 118개 동네의 MBTI 성격 프로필을 검색합니다. 동네 이름, 성격 특성, 분위기 등 텍스트 기반 검색에 사용하세요. 결과에는 구(SGG), 동(EMD), MBTI 유형, 성격 요약(CHARACTER_SUMMARY), 상세 프로필(PROFILE_TEXT)이 포함됩니다."
      }
    },
    {
      "tool_spec": {
        "type": "cortex_analyst_text_to_sql",
        "name": "query_dongne",
        "description": "동네 MBTI 데이터를 SQL로 조회합니다. 4축 점수(EI/SN/TF/JP), 평균 소득, 자산, 매매 시세, 방문인구 비율, 청년 비율 등 수치 데이터 조회에 사용하세요. MBTI 유형별 분포, 구별 비교, 유사 동네 찾기 등 분석 쿼리도 가능합니다."
      }
    }
  ],
  "tool_resources": {
    "search_dongne": {
      "execution_environment": {
        "query_timeout": 120,
        "type": "warehouse",
        "warehouse": "COMPUTE_WH"
      },
      "search_service": "DONGNE_MBTI.PUBLIC.DONGNE_SEARCH"
    },
    "query_dongne": {
      "execution_environment": {
        "query_timeout": 120,
        "type": "warehouse",
        "warehouse": "COMPUTE_WH"
      },
      "semantic_model_file": "@DONGNE_MBTI.PUBLIC.dongne_repo/branches/main/models/dongne_mbti.yaml"
    }
  }
}
$$;

-- 검증
SHOW AGENTS LIKE 'DONGNE_AGENT' IN SCHEMA DONGNE_MBTI.PUBLIC;
DESCRIBE AGENT DONGNE_MBTI.PUBLIC.DONGNE_AGENT;
