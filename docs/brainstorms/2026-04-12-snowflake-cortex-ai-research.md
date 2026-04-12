# Snowflake Cortex AI 리서치: "왜 Snowflake인가" 근거 자료

> 해커톤 발표용 | 2026-04-12 작성

---

## 1. AI_SENTIMENT - 감정 분석

### 벤치마크 (공식)

| 모델 | Aspect-Based (ABSA-mix) | ABSA 다국어 | Overall 감정 | Overall 다국어 |
|---|---|---|---|---|
| **Cortex AI_SENTIMENT** | **0.92** | **0.81** | **0.83** | **0.83** |
| Claude 4 Sonnet | 0.84 | 0.79 | 0.75 | 0.82 |
| Mistral Large 2 | 0.83 | 0.80 | 0.77 | 0.78 |
| GPT-4.1 | 0.83 | 0.73 | 0.80 | 0.78 |
| Llama 4 Scout | 0.82 | 0.79 | 0.71 | 0.76 |
| AWS DetectSentiment | - | - | 0.62 | 0.64 |

- **핵심 메시지**: Aspect-Based 감정 분석에서 92% 정확도로 Claude, GPT-4.1, AWS를 크게 앞섬
- 7개 언어 지원 (영어, 스페인어, 프랑스어, 독일어, 힌디어, 이탈리아어, 포르투갈어)
- positive/negative/neutral/**mixed**/unknown 5단계 분류 (mixed 감정 탐지가 차별점)
- 2025년 7월 GA

### 출처
- https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-sentiment
- https://docs.snowflake.com/en/release-notes/2025/other/2025-07-25-cortex-aisql-ai-sentiment

---

## 2. AI_CLASSIFY - 텍스트 분류

### 성능
- **학습 데이터 없이 80~90% 정확도** (zero-shot classification)
- 20개 이하 카테고리 권장 (초과 시 정확도 저하)
- 텍스트 + 이미지 모두 분류 가능 (멀티모달)
- task description, label description, examples로 정확도 향상 가능

### 핵심 장점
- 커스텀 모델 학습 없이 SQL 한 줄로 분류 파이프라인 구축
- 기존에 ML 팀이 몇 주 걸리던 작업을 즉시 처리

### 출처
- https://docs.snowflake.com/en/sql-reference/functions/ai_classify
- https://www.celestinfo.com/snowflake-cortex-ai-guide.html

---

## 3. AI_COMPLETE - 범용 텍스트 생성

### 지원 모델 (2025 기준)
- **대형**: Claude 3.7 Sonnet, Mistral Large 2 (SOTA급)
- **중형**: Claude 3.5 Sonnet, GPT-4.1 등
- **소형**: Llama 3.1-8B (128K 컨텍스트, 초저지연), Mistral-7B (32K)
- **Snowflake 자체**: Arctic 모델 패밀리

### 핵심 장점
- 모델 선택의 유연성: 작업 복잡도에 맞는 모델 선택 -> 비용 최적화
- SQL 내에서 직접 호출 (`SELECT AI_COMPLETE(...)`)
- Temperature, top_p 등 하이퍼파라미터 제어 가능

### 출처
- https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql

---

## 4. Cortex Analyst - NL2SQL (자연어 -> SQL)

### 벤치마크

| 비교 대상 | 정확도 |
|---|---|
| **Cortex Analyst** | **90%+** (실제 BI 시나리오) |
| GPT-4o (단일 프롬프트) | ~45% (Cortex 대비 약 2배 낮음) |
| 기타 시장 솔루션 | ~76% (Cortex 대비 14% 낮음) |
| Arctic-Text2SQL-R1.5 | GPT-5, Claude Sonnet 4.5, Gemini 2.5 Flash 대비 정확도 + 속도 모두 우위 |
| AtScale 시맨틱 레이어 적용 시 | **100%** (벤치마크 기준) |

### 핵심 차별점
- **시맨틱 모델(YAML)** 기반 -> 비즈니스 로직/메트릭 정의를 이해
- 단순 스키마만 보는 GPT-4o와 달리, 비즈니스 컨텍스트를 반영한 SQL 생성
- "forecast accuracy"같은 비즈니스 용어도 시맨틱 모델에 정의된 대로 해석
- **Arctic-Text2SQL-R1.5**: Snowflake SQL 특화 모델, Sonnet 4.5 대비 3배 빠른 지연시간
- Cortex Search 연동으로 고카디널리티 컬럼의 리터럴 매칭도 해결

### 출처
- https://www.snowflake.com/en/engineering-blog/cortex-analyst-text-to-sql-accuracy-bi/
- https://www.snowflake.com/en/engineering-blog/real-time-text-to-sql-snowflake-intelligence/
- https://www.atscale.com/blog/semantic-layer-cortex-analyst-accuracy/

---

## 5. Cortex Search - 하이브리드 검색 (RAG)

### 벤치마크

| 검색 방식 | NDCG@10 |
|---|---|
| Lexical (키워드) | 0.22 |
| Vector (벡터) | 0.49 |
| Hybrid (벡터+키워드) | 0.53 |
| **Hybrid + Reranker (Cortex Search)** | **0.59** |

- 단순 벡터 검색 대비 **12% 이상 검색 품질 향상**
- 키워드 검색 대비 약 **2.7배** 품질 향상
- 쿼리 응답 시간: **200~300ms** (대규모 텍스트 대상)

### 핵심 구성
- **Arctic Embed M** 기반 벡터 검색 + 키워드(BM25) 검색 + 시맨틱 리랭킹
- Elasticsearch/Azure AI Search 등 Lucene 기반 경쟁 서비스 대비 out-of-the-box 성능 우위
- 자동 인덱스 갱신 (5분~1일 단위 설정 가능)
- 별도의 벡터 DB 불필요 (Pinecone, Weaviate 등 대체)

### 출처
- https://www.snowflake.com/en/blog/cortex-search-ai-hybrid-search/
- https://www.snowflake.com/en/engineering-blog/cortex-search-and-retrieval-enterprise-ai/
- https://www.snowflake.com/en/engineering-blog/cortex-search-unmatched-quality-simplicity/

---

## 6. ML FORECAST - 시계열 예측

### 기술 스펙
- **알고리즘**: Gradient Boosting Machine (GBM) + ARIMA 결합
- 단일/다중 시리즈 예측 지원
- 외생 변수(exogenous variables) 포함 가능
- 95% 예측 구간(prediction interval) 기본 제공
- SQL 기반 (모델 학습 + 예측 모두 SQL로 완료)

### 정확도
- 공식 벤치마크 수치 미공개, 그러나:
  - Cortex/Prophet 기반 모델: **MAPE 10~15% 이하** (안정적 환경 기준, FinOps Foundation 기준)
  - SpartanNash 사례: 기존 방식 대비 **수 퍼센트포인트 향상**, 매주 5분 내 자동 예측 (기존 수시간)

### 출처
- https://docs.snowflake.com/en/user-guide/ml-functions/forecasting
- https://coalesce.io/product-technology/automate-building-snowflake-cortex-ml-functions-in-coalesce/

---

## 7. 실제 활용 사례

### 엔터프라이즈 사례

| 기업 | 활용 | 성과 |
|---|---|---|
| **Penske Logistics** | Cortex AI로 LLM 기반 요약 모델 구축 | 15일 만에 개발, 30+컬럼 수동 분석 제거, 직원 안전/리텐션 개선 |
| **Alberta Health Services** | ER 환자 방문 녹음 -> 전사 -> 요약 자동화 | **환자 15% 더 진료** (의사 노트 작성 시간 절감) |
| **TS Imagine** | 10만 이메일/6만 티켓 모니터링 자동화 | **비용 30% 절감**, 4,000시간 이상 절약 |
| **Bayer** | Cortex Analyst로 자연어 데이터 접근 | 비기술 부서까지 셀프서비스 데이터 접근 확대 |
| **BlackRock** | 고객 포트폴리오/통화 이력 분석 | 고객별 맞춤 인사이트 즉시 제공 |
| **Harkins Builders** | 턴오버 내러티브 자동 생성 | 1시간+ -> 수분으로 단축 |
| **Firework** | AI 가상 쇼핑 어시스턴트 | 개인화된 1:1 쇼핑 경험 제공 |
| **SpartanNash** | ML FORECAST로 수요 예측 | 수시간 -> 5분, 정확도 향상 |
| **Lumilinks** (Startup Challenge 2025 우승) | Cortex + Document AI + Streamlit | 차량 오프로드 시간 30% 감소 (7자리 수 비용 절감) |

### 수상 이력
- **CRN Tech Innovator Awards**: AI Software 부문 수상 (2025)
- **Snowflake Startup Challenge 2025 우승**: Lumilinks (FleetSense AI)
- **RAG 'n' ROLL 해커톤** (Snowflake x Mistral): Cortex Search + Mistral + Streamlit 기반 (상금 $10,000)

### Snowflake 내부 사례
- **500+ Streamlit 앱** 내부 운영 중 (2025년 6월 기준)
- 100+ 기여자, 재무/보안/제품분석 전 부서 활용
- GitLab: 수십 개 산발적 Streamlit 앱 -> 통합 엔터프라이즈 프레임워크로 전환

### 출처
- https://www.snowflake.com/en/customers/all-customers/case-study/penske/
- https://www.snowflake.com/en/blog/gen-ai-cortex-customer-stories-outcomes/
- https://www.snowflake.com/en/blog/secrets-gen-ai-success-real-world-stories/
- https://www.snowflake.com/en/blog/startup-challenge-2025-winner/
- https://www.snowflake.com/en/engineering-blog/scaling-enterprise-analytics-streamlit-apps/

---

## 8. Snowflake vs 대안 비교

### Snowflake Cortex vs Databricks AI vs BigQuery ML

| 비교 항목 | Snowflake Cortex | Databricks AI | BigQuery ML |
|---|---|---|---|
| **AI 접근 방식** | "AI를 서비스로 소비" - SQL로 호출 | "AI를 시스템으로 엔지니어링" - 모델 학습/파인튜닝 | Vertex AI 연동, SQL ML |
| **최적 대상** | BI + AI 통합, SQL 중심 팀 | 커스텀 AI 앱, 에이전트, 대규모 RAG | GCP 네이티브 분석 |
| **사용 편의성** | 높음 (SQL 한 줄) | 중간 (Spark 학습 필요) | 높음 (GCP 종속) |
| **거버넌스** | 네이티브 통합 (Horizon Catalog) | Unity Catalog (별도 구성) | GCP IAM |
| **멀티클라우드** | AWS/Azure/GCP | AWS/Azure/GCP | GCP Only |
| **비용 모델** | 크레딧 기반 + 토큰 과금 | DBU 기반 (복잡) | 쿼리 기반 과금 |

### "왜 Snowflake인가" 핵심 논거

#### 1. 데이터가 플랫폼 밖으로 나가지 않음
- **"Bring AI to data, not data to AI"** 철학
- 모든 AI 처리가 Snowflake 보안 경계 내에서 수행
- RBAC, 행 수준 보안, 데이터 마스킹 정책이 AI 워크로드에도 자동 적용
- 별도의 벡터 DB, ML 인프라, 데이터 파이프라인 불필요

#### 2. SQL 기반 접근성
- `SELECT AI_SENTIMENT(review_text) FROM reviews` -- 한 줄이면 감정 분석 완료
- 데이터 엔지니어, 분석가 누구나 AI 기능 활용 가능
- 별도 ML 전문가 없이도 80~92% 정확도의 AI 파이프라인 구축

#### 3. 통합 플랫폼
- 데이터 수집 -> 변환 -> AI 분석 -> 시각화(Streamlit) -> 공유까지 올인원
- Cortex Search + Cortex Analyst + ML Functions + Streamlit이 하나의 거버넌스 아래 통합
- 별도 인프라 운영 비용/복잡성 제거

#### 4. 엔터프라이즈 규모에서 검증됨
- AI가 Snowflake 고객 프로젝트의 **25%** 차지 (2025 Q2)
- 매주 **6,100+ 계정**이 AI 기능 활용
- 신규 로고의 **50%**가 AI 기능이 Snowflake 선택 이유

### 출처
- https://snowstack.ai/blog/databricks-vs-snowflake-2025-comparison
- https://aztela.com/articles/snowflake-vs-databricks-vs-bigquery-2025-comparison
- https://cloudwars.com/ai/ai-powering-25-of-snowflake-customer-projects-revenue-jumps-32/
- https://www.snowflake.com/en/blog/intelligent-governed-ai-at-scale/

---

## 발표 슬라이드용 한 줄 요약

| 기능 | 한 줄 킬러 스탯 |
|---|---|
| AI_SENTIMENT | 92% 정확도 - GPT-4.1, Claude, AWS 모두 능가 |
| AI_CLASSIFY | 학습 없이 80~90% 정확도, SQL 한 줄 |
| Cortex Analyst | 90%+ NL2SQL 정확도, GPT-4o 대비 2배 |
| Cortex Search | 벡터 검색 대비 12%+ 품질 향상, 200ms 응답 |
| ML FORECAST | SQL만으로 시계열 예측, MAPE 10~15% |
| 보안/거버넌스 | 데이터가 플랫폼 밖으로 절대 나가지 않음 |
| 채택률 | 6,100+ 계정이 매주 AI 사용, 신규 고객 50%가 AI 때문에 선택 |
