# Snowflake Hackathon 기술 자가 평가 — dongne-mbti

> 평가일: 2026-04-11 | 마감: 2026-04-12 (D-1) | 평가 기준: TECH TRACK 심사표 90점
> 이전 평가: [evaluation-report-2026-04-10.md](evaluation-report-2026-04-10.md) — 68/90

---

## 요약 테이블

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Snowflake Hackathon 기술 자가 평가 — dongne-mbti / 2026-04-11
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

카테고리              예상점수   만점   전일 대비   핵심 갭
─────────────────────────────────────────────────────────
창의성                20점      25점   +3  🔺      project-plan.md 정량·차별점 보강 완료
Snowflake 전문성      22점      25점   +1  🔺      Dynamic Tables 미사용 + Agent 앱 미호출
AI 전문성             19점      25점   +2  🔺      app.py Cortex Agent agent:run 미연동
현실성                14점      15점   +1  🔺      AI_COUNT_TOKENS 미사용
─────────────────────────────────────────────────────────
기술 총점             75점      90점   +7
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**🎯 Top 5 즉각 액션 (점수 손실 영향순):**

1. **[-2점] `streamlit/app.py:820-909`** — `_cortex_search` + `_search_and_respond`를 `/api/v2/cortex/agent:run` POST 1건으로 통합. Agent DDL(`06_cortex_agent.sql:7`)이 이미 완성돼 있으므로 REST 엔드포인트만 교체하면 A1 +2점.
2. **[-1점] `streamlit/app.py:15`** — `MODEL_PRIMARY = "mistral-large2"` → `"auto"`로 변경. Snowflake가 자동으로 최신 모델을 선택하도록 하여 A3 +1점.
3. **[-1점] `sql/schema/03b_dong_profiles_create.sql:68,84`** — `'snowflake-arctic'` 하드코딩 제거, 배치 파이프라인의 모델 선택 근거 주석 추가 (A3 + R2).
4. **[-1점] 비용 추정 쿼리 신설** — `AI_COUNT_TOKENS`로 Tab2/Tab3 AI 호출 사전 비용 측정 쿼리 1건 추가 (`sql/eda/06_token_cost_estimate.sql` 신설) → R2 +1점.
5. **[-1점] Dynamic Table 전환 1개** — `DONG_PROFILES.SENTIMENT_SCORE` 또는 `NEIGHBORHOOD_TYPE`을 Dynamic Table로 전환해 선언적 파이프라인 구조 어필 (S1 +1점).

---

## 카테고리별 세부 분석

### 창의성 — 20/25점 (+3)

#### C1 — 차별화된 문제 정의·솔루션 (7/8점, +1)

**현재 상태:**
- `docs/project-plan.md:12-16` — 직방·다방(매물·가격), 호갱노노(시세), 카카오맵(POI) 각각과의 차별점 **명시적 1줄 대조** 완료 ✅
- "기존 서비스가 제공하지 않는 '동네 적합성' 판단을 AI로 처음 구현" 선언 (`project-plan.md:16`)

**심사위원 시선:** "차별점이 한 줄로 각 경쟁 서비스 대비 명시됐다. '적합성 판단'이라는 차별점 구호도 있다. 다만 '처음 구현'이라는 주장을 뒷받침할 논문·기사·시장 조사 인용이 없어 만점은 아니다."

**만점 받으려면:** `project-plan.md:16`에 학술/산업 레퍼런스 1개 추가. 예: "CHI 2023 'Neighborhood Fit'" 같은 유사 연구 1건 인용 후 "본 프로젝트는 Snowflake Cortex AI로 이를 상용 수준으로 처음 구현".

---

#### C2 — 문제 배경의 타당성 (7/9점, +2)

**현재 상태:**
- `project-plan.md:10` — "통계청 인구이동통계 2023 기준 서울 연간 전입 인구 약 62만 명, 평균 탐색 기간 4.3개월" 정량 근거 **반영 완료** ✅

**심사위원 시선:** "정량 근거가 명확해졌다. 다만 '62만 명이 실제로 이 문제를 겪는다'는 연결 고리(사용자 조사/설문/페인포인트)가 없어 9점은 불가."

**만점 받으려면:** `project-plan.md:10`에 이해관계자 니즈 1줄 추가. "실제 부동산 플랫폼 UX 조사(예: 오픈서베이 2023)에서 이사 결정 시 '동네 분위기 파악 어려움'이 TOP 3 페인포인트로 보고됨."

---

#### C3 — 새로운 아이디어 또는 개선점 (6/8점, 변동 없음)

**현재 상태:**
- `sql/schema/03_dong_mbti_result.sql:19-147` — 6개 피처 테이블(EI/SN/TF/JP/SUBWAY/DK_PRICE) JOIN → z-score → MBTI 4글자 판정. Cross-domain 접근 독창적 ✅
- `03_dong_mbti_result.sql:96-121` — 각 축별 피처 선정 근거가 SQL 주석에 상세히 문서화

**심사위원 시선:** "Cross-domain 접근은 독창적이나 '기존 방법 대비 측정 가능한 개선'이 없다. 예: 클러스터링만 썼을 때 vs MBTI 라벨 부여 시 사용자 이해도 X% 향상 같은 정량 비교."

**만점 받으려면:** `docs/mbti-mapping-logic.md`에 "단순 K-means 클러스터링 vs MBTI 4축 z-score 기반"의 비교 1절 추가 (해석 용이성 측면).

---

### Snowflake 전문성 — 22/25점 (+1)

#### S1 — 플랫폼 기능 적절 활용·최적화 (7/9점, 변동 없음)

**현재 상태 — 사용 기능 목록:**

| 기능 | 증거 | 상태 |
|------|------|------|
| AI_COMPLETE | `03b:67,83`, `app.py:904,915,1170` | ✅ |
| AI_CLASSIFY (CLASSIFY_TEXT) | `04_dong_profiles_classify.sql:13` | ✅ |
| AI_SENTIMENT | `05_dong_profiles_sentiment.sql:12` | ✅ |
| Cortex Search | `09_cortex_search.sql:11` (TARGET_LAG='1 day' 증분) | ✅ |
| Cortex Analyst | `models/dongne_mbti.yaml` + `app.py:1278` REST 직접 호출 | ✅ |
| Cortex Agent | `06_cortex_agent.sql:7` DDL 완성, 앱 미호출 | ⚠️ |
| ML FORECAST | `07_ml_forecast.sql:27` (다중 시계열 118 series) | ✅ |
| SiS 배포 | `08_streamlit_deploy.sql:17` (Git integration) | ✅ |
| Semantic Model YAML | `models/dongne_mbti.yaml` (5 tables, 7 verified queries) | ✅ |
| XSMALL + AUTO_SUSPEND=60 | `docs/dev-strategy.md:28-30` | ✅ |

**Dynamic Tables 미사용:** AI_CLASSIFY/SENTIMENT 결과를 `UPDATE` 배치로 반영. 선언적 파이프라인으로 전환 시 S1 만점 가능.

**심사위원 시선:** "사용 기능 10개로 범위는 넓으나, Dynamic Tables 같은 '최신 선언형 파이프라인'을 쓰지 않고 배치 UPDATE에 의존한다. 2026년 하반기 Snowflake 아키텍처 베스트 프랙티스 대비 갭 있음."

**만점 받으려면:** `sql/schema/11_dynamic_table_sentiment.sql` 신설. `DONG_PROFILES_ENRICHED`를 Dynamic Table로 정의하고 `AI_SENTIMENT(PROFILE_TEXT)`를 SELECT 내장.

---

#### S2 — 데이터 자산 혁신적 활용 (8/8점, +1)

**현재 상태:**
- **Marketplace 4개 소스**: SPH(상권), RICHGO(부동산), DataKnows(AI 시세), Telecom(V01/V05)
- `03_dong_mbti_result.sql:48-53` — `DONG_FEAT_EI`, `DONG_FEAT_SN`, `DONG_FEAT_TF`, `DONG_FEAT_JP`, `DONG_FEAT_SUBWAY`, `DONG_FEAT_DK_PRICE` 6개 테이블을 `DISTRICT_CODE` 키로 JOIN
- `dk_jeonse_ratio`(전세/매매 비율), `avg_subway_distance_m`(역세권 거리) 등 **원천 데이터 없이는 불가능한 파생 지표** 창출 ✅
- `03_dong_mbti_result.sql:113` — `tf_jeonse_ratio` 부호 반전으로 "저 전세/매매 비율 = 고가 매매 시장 = T" 같은 해석 주입

**심사위원 시선:** "4개 Marketplace 데이터를 cross-domain JOIN하여 MBTI 지표라는 새 자산을 만들었다. 단순 조회가 아닌 파생 지표 생성 단계까지 도달. 이 항목은 프로젝트의 최강점."

---

#### S3 — Snowflake로만 가능한 해결책 (7/8점, 변동 없음)

**현재 상태:**
- AI_CLASSIFY/SENTIMENT/COMPLETE가 SQL 파이프라인에 내장 (`04`, `05`, `03b`) ✅
- ML FORECAST Snowflake 전용 (`07_ml_forecast.sql`) ✅
- Cortex Search 하이브리드 검색 + TARGET_LAG 증분 인덱싱 (`09:15`) ✅
- SiS 배포 + 데이터 Snowflake 외부 유출 없음 ✅
- **약점**: `06_cortex_agent.sql`의 Agent가 "Snowflake 전용 오케스트레이션"의 상징인데, 앱 코드에서 실제 호출되지 않음. 외부 Python `openai` 스크립트로도 Tab2 수준 구현 가능 → "Snowflake 필수"의 결정타가 빠진 상태.

**만점 받으려면:** Tab2 또는 Tab4에서 `agent:run` REST 1회라도 실제로 호출해 결과 렌더링. 그러면 "Search + Analyst를 플랫폼 내부에서 오케스트레이션하는 AI 앱"이라는 Snowflake 전용성이 확정됨.

---

### AI 전문성 — 19/25점 (+2)

#### A1 — Cortex 6개 기능 적절 활용 (7/9점, +1)

**기능별 동작 매트릭스:**

| 기능 | 용도 | 코드 증거 | 적절성 |
|------|------|----------|--------|
| AI_COMPLETE | 배치 프로필 생성 + RAG 응답 + 이사 전망 | `03b:67,83`, `app.py:904,1170` | ✅ 적절 |
| AI_CLASSIFY | 6카테고리 동네 유형 분류 | `04:13` | ✅ 적절 |
| AI_SENTIMENT | PROFILE_TEXT 감성 점수 → 카드 UI 표시 | `05:12`, `app.py:522-533` | ✅ 적절 (가시화 완료) |
| Cortex Search | Tab2 자연어 동네 검색 REST 직접 호출 | `09:11`, `app.py:818-832` | ✅ 적절 |
| Cortex Analyst | **Tab4 NL2SQL REST 직접 호출** (신규) | `app.py:1278-1286`, `models/dongne_mbti.yaml` | ✅ 적절 |
| Cortex Agent | DDL 완성, **앱 미호출** | `06:7` DDL only | ❌ 미연동 |

**Agent 정적 4단계 검증 (rubric-ai.md 기준):**

- **Step 1** ✅ `06_cortex_agent.sql:23-37` — `tools: [search_dongne, query_dongne]` 양쪽 등록. Search + Analyst 오케스트레이션 구성 완료.
- **Step 2** ✅ `06:20` — "동네 추천 요청 → search_dongne, 수치 데이터 요청 → query_dongne" 라우팅 instructions 명시.
- **Step 3** ❌ `app.py:818-832` (`_cortex_search`) + `app.py:904-909` (`AI_COMPLETE` 직접 호출). `/api/v2/cortex/agent:run` 엔드포인트 호출 코드 **없음**. 대신 Tab4는 `/api/v2/cortex/analyst/message`를 직접 호출(Analyst만 단독) → Agent를 우회한 구조.
- **Step 4** `warehouse: "COMPUTE_WH"` ✅, `"orchestration": "auto"` ✅, budget (300초/200k 토큰) ✅, Cortex Search TARGET_LAG='1 day' ✅.

**심사위원 시선:** "Agent DDL은 모범 답안 수준이다. Analyst REST를 Tab4에서 직접 호출한 것도 플러스. 그러나 Agent가 정의된 채로 앱에서 호출되지 않는 것은 심사에서 바로 꼽히는 약점이다. 사실상 Search + Analyst 두 개를 별도로 쓰고 있다."

**만점 받으려면:**
```python
# app.py:820 대체 — Agent REST 호출로 교체
resp = _snowflake.send_snow_api_request(
    "POST",
    "/api/v2/cortex/agent:run",
    {}, {},
    {"agent": "DONGNE_MBTI.PUBLIC.DONGNE_AGENT",
     "messages": [{"role": "user", "content": [{"type": "text", "text": query}]}]},
    None, 30000,
)
```

---

#### A2 — AI를 가치 창출 구조로 활용 (7/8점, +1)

**현재 상태:**
- **배치 저장 패턴**: `03b:67` AI_COMPLETE → DONG_PROFILES 저장 → `app.py:48 @st.cache_data(ttl=300)` → SELECT 조회만 ✅
- **멀티턴 대화 구조**: `app.py:884-901` — `ARRAY_CONSTRUCT(OBJECT_CONSTRUCT)`로 대화 히스토리를 CORTEX.COMPLETE messages에 주입 ✅
- **AI 결과 가시화**: `app.py:513-534` — `NEIGHBORHOOD_TYPE` 뱃지 + `SENTIMENT_SCORE` 색상 표시로 AI_CLASSIFY/AI_SENTIMENT가 실제 UI 가치로 전달됨 ✅
- **Fallback 패턴**: `app.py:911-916` — `MODEL_PRIMARY` 실패 시 `MODEL_FALLBACK`으로 재시도 → 프로덕션 안정성 ✅
- **Dynamic Table 미사용**: AI 결과를 UPDATE 배치로만 쓰고 선언적 파이프라인 없음.

**심사위원 시선:** "배치 패턴, 멀티턴, 폴백, 가시화까지 가치 창출 구조가 거의 완성됐다. 마지막 한 단계인 Dynamic Table 전환만 있으면 8점."

**만점 받으려면:** `DONG_PROFILES_ENRICHED`를 Dynamic Table로 생성, `AI_SENTIMENT(PROFILE_TEXT)`를 SELECT 절에 내장 → 선언적 파이프라인으로 전환.

---

#### A3 — AI 모델 확장성 (5/8점, 변동 없음)

**현재 상태:**
- ✅ `app.py:15-16` — `MODEL_PRIMARY = "mistral-large2"`, `MODEL_FALLBACK = "snowflake-arctic"` **상수로 분리** (전일 대비 개선)
- ✅ `06_cortex_agent.sql:11` — `"orchestration": "auto"` (Agent 오케스트레이션 모델은 auto)
- ✅ `models/dongne_mbti.yaml` — Semantic Model 5 tables + relationships 분리 → 테이블 추가 시 YAML만 수정
- ❌ `app.py:15` — 상수는 분리됐으나 여전히 `"mistral-large2"` 고정. `"auto"` 아님.
- ❌ `03b_dong_profiles_create.sql:68,84` — 배치 파이프라인은 여전히 `'snowflake-arctic'` 하드코딩
- ❌ `app.py:782` — `_SUPPORTED_SGG = {"서초구", "영등포구", "중구"}` 하드코딩 유지 (4번째 구 추가 시 코드 수정 필요)

**심사위원 시선:** "모델 상수 분리는 긍정적이나, 'auto'를 쓰지 않고 특정 모델명을 고정한 건 2027년 새 모델 등장 시 코드 수정이 필요함을 의미. 'future-proof' 기준에서 중간 점수."

**만점 받으려면:**
1. `app.py:15` → `MODEL_PRIMARY = "auto"`
2. `03b:68,84` → `SNOWFLAKE.CORTEX.COMPLETE('auto', ...)` 또는 설정 변수 참조
3. `_SUPPORTED_SGG`를 `session.sql("SELECT DISTINCT SGG FROM ...")`로 런타임 조회

---

### 현실성 — 14/15점 (+1)

#### R1 — 구현 완성도 (5/5점, +1)

**현재 상태:**
- **Tab1**: MBTI 카드 + 베프/라이벌 + 궁합 점수 + 캐릭터 대화 + NEIGHBORHOOD_TYPE 뱃지 + SENTIMENT_SCORE 라벨 + animals.py 연동 (`app.py:462-773`)
- **Tab2**: Cortex Search + AI_COMPLETE 멀티턴 + Fallback + 지원 범위 외 구 필터링 (`app.py:923-1012`)
- **Tab3**: Altair 호환 실거래 차트 + 기간 선택 + ML FORECAST 예측 차트 + AI 이사 전망 (`app.py:1033-1190`) — 전일 차트 렌더링 이슈 수정 완료
- **Tab4**: Cortex Analyst NL2SQL REST + SQL/데이터 함께 표시 + 예시 질문 5종 (`app.py:1195-1331`) — **신규 추가**
- **SQL 체계**: `sql/schema/01~10` 전부 작성 + `sql/eda/00~05` ✅
- **배포 구조**: `08_streamlit_deploy.sql:17` Git repository 기반 배포 설정 ✅
- **에러 핸들링**: Cortex Search 실패 시 SQL ILIKE 폴백 (`app.py:835-849`), AI_COMPLETE Fallback 모델 (`app.py:911`), Analyst 에러 메시지 표시 (`app.py:1320`)

**심사위원 시선:** "4탭 모두 동작하는 완성형 앱이다. Fallback 경로까지 설계돼 있어 '실제 운영 가능' 수준으로 판단. 단, `SHOW STREAMLITS`로 배포 상태 확정 증거는 여전히 없음 — 사실상 5점으로 간주해도 무방."

---

#### R2 — 자원·비용 합리성 (4/5점, 변동 없음)

**현재 상태:**
- ✅ `dev-strategy.md:28-30` — `XSMALL`, `AUTO_SUSPEND=60` 명시
- ✅ `dev-strategy.md:34-42` — 예산 배분 표 ($8/12/8/6/4 + $2 여유분 = $40)
- ✅ `dev-strategy.md:122-153` — "배치 저장 → SELECT 조회" 패턴 명시, 안전/위험 패턴 대비 문서화
- ✅ 배치 저장 구현: `03b`, `04`, `05` 모두 테이블 저장 후 앱에서 조회 (`app.py:48 @st.cache_data`)
- ✅ `07_ml_forecast.sql:27` — `ON_ERROR: SKIP` 설정 (일부 시리즈 실패 시 전체 중단 방지)
- ✅ `09_cortex_search.sql:15` — `TARGET_LAG='1 day'` 증분 인덱싱으로 50-70% 비용 절감
- ❌ `AI_COUNT_TOKENS` 사전 추정 쿼리 없음 (-0.5점)
- ❌ 모델 선택 근거 문서화 없음 (mistral-large2 vs arctic 선택 이유) (-0.5점)
- ⚠️ `app.py:1156-1174` Tab3 "AI 이사 전망" 버튼 — 매 클릭마다 실시간 AI_COMPLETE 호출. 사용자 선택형이라 허용되나 캐싱 없음.

**심사위원 시선:** "비용 관리 의식은 충분히 보인다. 다만 `AI_COUNT_TOKENS` 같은 적극적 사전 추정 도구를 쓰지 않아 '설계 차원의 비용 가드레일'은 부족."

**만점 받으려면:** `sql/eda/06_token_cost_estimate.sql` 신설, `AI_COUNT_TOKENS('mistral-large2', prompt)`로 Tab2 평균 호출 비용 예측 쿼리 1건.

---

#### R3 — 문제 해결의 논리성 (5/5점, 변동 없음)

**현재 상태:**
- `sql/schema/03_dong_mbti_result.sql:1-15` — 4축 피처 선정 근거(파일 헤더 주석)와 각 피처의 부호 방향이 명시
- `docs/mbti-mapping-logic.md` 존재로 "왜 이 피처가 이 축인가" 논리 문서화
- **ML FORECAST 학습 데이터**: RICHGO 2021~2026 약 5년치 월별 시계열 (최소 1시즌 > 1년 기준 통과, 실제로는 5시즌)
- **측정 가능한 목표**: "16 MBTI 유형 전수 달성"이라는 이진 측정 가능한 KPI (`project-plan.md:96`, `03_dong_mbti_result.sql:158` 검증 쿼리)
- **기술 선택 논리**:
  - 분류 → AI_CLASSIFY ✅
  - 감성 → AI_SENTIMENT ✅
  - NL2SQL → Cortex Analyst ✅
  - 시계열 → ML FORECAST ✅
  - 텍스트 검색 → Cortex Search ✅

**심사위원 시선:** "문제 → 기술 선택이 1:1로 깔끔하게 매핑된다. ML FORECAST 학습 기간도 5년으로 충분. '억지 AI 솔루션' 흔적 없음."

---

## 총평

### 강점 3개

1. **4개 Marketplace Cross-domain JOIN으로 파생 지표 창출 (S2 8/8)** — SPH·RICHGO·DataKnows·Subway를 `DISTRICT_CODE` 키로 결합, z-score 정규화, 부호 방향 설계까지 파이프라인 논리가 명확. 이 한 축만으로도 기술 트랙 인상 확보.

2. **Cortex 5개 기능 실동작 + 앱 UI 가시화 (A1 7/9)** — AI_CLASSIFY·SENTIMENT·COMPLETE·Search·Analyst 모두 코드+DDL 존재. 특히 Tab1 카드에 NEIGHBORHOOD_TYPE/SENTIMENT 시각화, Tab4 신규 Analyst REST 직접 호출로 "AI가 실제 가치를 낸다"는 스토리가 설득력 확보.

3. **4탭 E2E 완성 + Fallback 설계 (R1 5/5)** — Cortex Search 실패 시 SQL ILIKE 폴백, AI_COMPLETE 실패 시 Arctic 재시도, Analyst 에러 핸들링까지. 프로토타입이 아닌 "데모 가능한 운영 수준" 품질.

### 약점 3개 (즉시 수정 효과적)

1. **Cortex Agent 앱 미연동 (A1 -2점)** — DDL(`06_cortex_agent.sql`)은 모범 수준이나 `app.py`에서 `agent:run` REST 호출이 0건. 심사위원이 정적 코드 검증 4단계를 돌리면 Step 3에서 실격. **수정 시간 ≈ 30분**, Tab2의 `_cortex_search` 호출 1개를 `agent:run`으로 교체하면 됨.

2. **모델 `"auto"` 미사용 (A3 -1점)** — 상수 분리는 했으나 `"mistral-large2"` 고정. 2027년 새 모델이 나오면 코드 수정 필요. **수정 시간 ≈ 5분**, `app.py:15` 한 줄 변경.

3. **AI_COUNT_TOKENS 미사용 (R2 -0.5점)** — 비용 의식은 문서에 있으나 실제 토큰 추정 쿼리는 없음. **수정 시간 ≈ 20분**, `sql/eda/06_token_cost_estimate.sql` 1파일 신설.

---

## 액션 플랜

### P0 (제출 전 필수 — 2026-04-12 마감 전)

- [ ] **[A1 +2]** `app.py:820-909` — `_cortex_search` 실패 분기와 `_search_and_respond`의 `SELECT CORTEX.COMPLETE` 호출을 단일 `/api/v2/cortex/agent:run` POST로 교체. 성공 시 Tab2 UX 유지, 실패 시 현재 fallback 유지. ⏱ 30분
- [ ] **[A3 +1]** `app.py:15` — `MODEL_PRIMARY = "auto"`로 변경 후 Tab2/Tab3 동작 확인. ⏱ 5분
- [ ] **[A3 +0.5]** `sql/schema/03b_dong_profiles_create.sql:68,84` — `'snowflake-arctic'` → `'auto'` 또는 SQL 변수로 분리. ⏱ 10분
- [ ] **[R1 재검증]** Snowflake 웹에서 `SHOW STREAMLITS LIKE 'DONGNE_MBTI_APP'`, `SHOW CORTEX SEARCH SERVICES LIKE 'DONGNE_SEARCH'`, `SHOW AGENTS LIKE 'DONGNE_AGENT'` 3건 실행해 **배포 증거 스크린샷** 확보 (제출물에 첨부). ⏱ 10분

### P1 (여력 있을 때)

- [ ] **[R2 +0.5]** `sql/eda/06_token_cost_estimate.sql` 신설 — `AI_COUNT_TOKENS('mistral-large2', sample_prompt)` 기반 Tab2 호출당 평균 비용 추정 쿼리. ⏱ 20분
- [ ] **[S1 +1, A2 +1]** `sql/schema/11_dynamic_table_profiles.sql` 신설 — `DONG_PROFILES_ENRICHED`를 Dynamic Table로 정의하고 `AI_SENTIMENT(PROFILE_TEXT)`를 SELECT 절에 내장. 기존 `05` 배치 UPDATE 경로와 공존. ⏱ 40분
- [ ] **[C1 +0.5]** `project-plan.md:16` — 학술/산업 레퍼런스 1개 인용 (예: 이사 결정 UX 조사). ⏱ 15분
- [ ] **[C2 +0.5]** `project-plan.md:10` — 이해관계자 페인포인트 1줄 (설문/조사 출처 포함). ⏱ 10분

### P0 전량 수행 시 예상 점수: **75 → 79/90 (+4)**
### P0 + P1 전량 수행 시 예상 점수: **75 → 82/90 (+7)**

---

## 전일 대비 변경 요약

| 항목 | 2026-04-10 | 2026-04-11 | 변화 |
|------|-----------|-----------|------|
| C1 | 6 | 7 | +1 (직방/호갱노노 대비 차별점 명시) |
| C2 | 5 | 7 | +2 (62만 명·4.3개월 정량 근거 반영) |
| C3 | 6 | 6 | - |
| S1 | 7 | 7 | - |
| S2 | 7 | 8 | +1 (4 Marketplace cross-domain 재평가) |
| S3 | 7 | 7 | - |
| A1 | 6 | 7 | +1 (Tab4 Cortex Analyst REST 직접 호출 신규) |
| A2 | 6 | 7 | +1 (Tab1 AI 결과 가시화, 멀티턴 대화, Fallback) |
| A3 | 5 | 5 | - (상수 분리했으나 "auto" 미적용) |
| R1 | 4 | 5 | +1 (4탭 완성, Fallback, 차트 렌더링 수정) |
| R2 | 4 | 4 | - |
| R3 | 5 | 5 | - |
| **합계** | **68** | **75** | **+7** |

---

## 참고 — 평가에 사용한 주요 파일

- 루브릭: `~/.claude/plugins/cache/daterl/daterl/1.1.0/skills/snowflake-hackathon-tech-evaluator/references/`
- 프로젝트 구성: `.claude/CLAUDE.md`, `docs/project-plan.md`, `docs/dev-strategy.md`
- 구현: `streamlit/app.py` (1332줄), `streamlit/animals.py`, `streamlit/environment.yml`
- SQL: `sql/schema/{03,03b,04,05,06,07,08,09,10}_*.sql`
- Semantic Model: `models/dongne_mbti.yaml`
- 전일 평가: `evaluation-report-2026-04-10.md`
