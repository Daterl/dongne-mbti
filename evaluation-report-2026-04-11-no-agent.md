# Snowflake Hackathon 기술 자가 평가 — dongne-mbti (Cortex Agent 제외)

> 평가일: 2026-04-11 | 마감: 2026-04-12 (D-1) | 평가 기준: TECH TRACK 심사표 90점
> 전제: **Cortex Agent 공식 미제공 → A1/S3 평가 범위에서 제외**
> 이전 평가(Agent 포함): `evaluation-report-2026-04-11.md` — 75/90

---

## 요약 테이블

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Snowflake Hackathon 기술 자가 평가 — dongne-mbti / 2026-04-11 (Agent 제외)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

카테고리              예상점수   만점   Agent 포함 대비   핵심 갭
─────────────────────────────────────────────────────────
창의성                20점      25점   ─               레퍼런스/경쟁 비교 부족
Snowflake 전문성      23점      25점   +1              Dynamic Table 미사용
AI 전문성             21점      25점   +2              모델 "auto" 미적용
현실성                14점      15점   ─               AI_COUNT_TOKENS 없음
─────────────────────────────────────────────────────────
기술 총점             78점      90점   +3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Agent 제외로 인한 점수 상향 근거:**
- **A1**: 5개 Cortex 기능(Complete/Classify/Sentiment/Search/Analyst) 전수 동작·용도 적절 → `rubric-ai.md:24` "5-6개 기능 모두 동작 + 각 기능이 적절한 용도"에 해당 → **7→9점 (+2)**
- **S3**: Agent 미호출이 유일한 약점이었으나 범위에서 제외됨. Search 하이브리드 + Analyst NL2SQL + ML FORECAST + SiS + TARGET_LAG 증분 인덱싱은 Snowflake 전용 → **7→8점 (+1)**

---

## 🎯 Top 5 즉각 액션 (Agent 제외 시 손실 영향순)

1. **[-2점] S1·A2 Dynamic Table 미사용** — `sql/schema/11_dynamic_table_profiles.sql` 신설, `DONG_PROFILES_ENRICHED`를 Dynamic Table로 정의하고 `AI_SENTIMENT(PROFILE_TEXT)`를 SELECT 절에 내장. S1 7→8, A2 7→8. ⏱ 40분
2. **[-1점] A3 모델 `"auto"` 미적용** — `streamlit/app.py:15` `MODEL_PRIMARY = "mistral-large2"` → `"auto"`. ⏱ 5분
3. **[-1점] A3 배치 파이프라인 모델 하드코딩** — `sql/schema/03b_dong_profiles_create.sql:68,84` `'snowflake-arctic'` → `'auto'`. ⏱ 10분
4. **[-0.5점] R2 AI_COUNT_TOKENS 미사용** — `sql/eda/06_token_cost_estimate.sql` 신설, Tab2/Tab3 호출당 평균 비용 추정 1건. ⏱ 20분
5. **[-1점] C1·C2 레퍼런스/페인포인트 조사 부족** — `docs/project-plan.md:10,16`에 학술·산업 조사 인용 1개씩 추가. ⏱ 25분

P0 전량 수행 시: **78 → 82~83/90 (+4~5)**

---

## 카테고리별 세부 분석

### 창의성 — 20/25점

#### C1 — 차별화된 문제 정의·솔루션 (7/8점)

**현재 상태**
- `docs/project-plan.md:12-16` — 직방·다방·호갱노노·카카오맵 4개 경쟁 서비스 대비 1줄 대조 완료
- "동네 적합성 판단을 AI로 처음 구현" 포지셔닝 (`project-plan.md:16`)

**심사위원 시선**: 한 줄 대조는 명확하나 '처음'이라는 주장을 뒷받침할 학술·시장 조사 인용이 없음.

**만점 받으려면**: `project-plan.md:16`에 학술 레퍼런스 1개 추가 (예: "CHI 2023 Neighborhood Fit 유사 연구" 같은 선행 연구 인용 후 "Snowflake Cortex AI로 상용화 최초" 주장).

---

#### C2 — 문제 배경의 타당성 (7/9점)

**현재 상태**
- `project-plan.md:10` — "통계청 인구이동통계 2023 기준 서울 연간 전입 62만 명, 평균 탐색 기간 4.3개월" 정량 근거 반영됨

**심사위원 시선**: 거시 통계는 명확. 다만 '62만 명이 실제로 이 페인포인트를 겪는다'는 미시적 연결 고리(설문/UX 조사)가 없어 9점 불가.

**만점 받으려면**: 페인포인트 조사 1줄 인용 (예: "오픈서베이 2023 부동산 UX 조사에서 '동네 분위기 파악 어려움'이 이사 결정 TOP 3 페인포인트").

---

#### C3 — 새로운 아이디어 또는 개선점 (6/8점)

**현재 상태**
- `sql/schema/03_dong_mbti_result.sql:19-147` — 6개 피처 테이블(EI/SN/TF/JP/SUBWAY/DK_PRICE) cross-domain JOIN → z-score 정규화 → MBTI 4글자 판정
- `03_dong_mbti_result.sql:96-121` — 각 축별 피처 선정 근거가 SQL 주석에 상세 문서화

**심사위원 시선**: Cross-domain 접근은 독창적. 그러나 '기존 방법(단순 클러스터링·지역 레이블) 대비 측정 가능한 개선' 증거가 없음.

**만점 받으려면**: `docs/mbti-mapping-logic.md`에 "K-means 클러스터링 vs MBTI 4축 z-score"의 해석 용이성 비교 1절 추가.

---

### Snowflake 전문성 — 23/25점

#### S1 — 플랫폼 기능 적절 활용·최적화 (7/9점)

**사용 기능 매트릭스 (Agent 제외)**

| 기능 | 증거 | 상태 |
|------|------|------|
| AI_COMPLETE | `03b:67,83`, `app.py:905,1170` | ✅ |
| AI_CLASSIFY | `04_dong_profiles_classify.sql:13` | ✅ |
| AI_SENTIMENT | `05_dong_profiles_sentiment.sql:12` | ✅ |
| Cortex Search | `09_cortex_search.sql:11` TARGET_LAG='1 day' | ✅ |
| Cortex Analyst | `models/dongne_mbti.yaml` + `app.py:1280` REST | ✅ |
| ML FORECAST | `07_ml_forecast.sql:27` 다중 시계열 118 series | ✅ |
| Semantic Model YAML | `models/dongne_mbti.yaml` 5 tables + 7 verified queries | ✅ |
| SiS + Git 배포 | `08_streamlit_deploy.sql:17` | ✅ |
| XSMALL·AUTO_SUSPEND=60 | `docs/dev-strategy.md:28-30` | ✅ |

**약점**: Dynamic Tables 미사용. AI_CLASSIFY/SENTIMENT 결과를 `UPDATE` 배치로 반영 → 선언적 파이프라인 구조 부재.

**만점 받으려면**: Dynamic Table 1개 신설 (Top Action #1).

---

#### S2 — 데이터 자산 혁신적 활용 (8/8점)

**현재 상태**
- **4개 Marketplace cross-domain**: SPH(상권)·RICHGO(실거래)·DataKnows(AI 시세)·Telecom(이사 추정)
- `03_dong_mbti_result.sql:48-53` — 6개 피처 테이블을 `DISTRICT_CODE` 키로 JOIN
- 파생 지표 창출: `dk_jeonse_ratio`(전세/매매 비율), `avg_subway_distance_m`(역세권 거리) 등 원천 데이터 없이는 불가능한 신규 자산
- `03:113` — `tf_jeonse_ratio` 부호 반전으로 "저 전세비 = 고가 매매 시장 = T" 해석 층 주입

**심사위원 시선**: 4 Marketplace를 cross-domain JOIN하여 MBTI 지표라는 새 자산 생성. 단순 조회가 아닌 파생 지표 단계까지 도달. **프로젝트 최강점**.

---

#### S3 — Snowflake로만 가능한 해결책 (8/8점, +1)

**Agent 제외로 인한 상향 근거**
- AI_CLASSIFY/SENTIMENT/COMPLETE를 SQL 파이프라인에 내장 (`04`, `05`, `03b`) — 외부 API로는 DB 왕복 없이 불가능
- Cortex Search 하이브리드(벡터+키워드) + TARGET_LAG 증분 인덱싱 (`09:15`) — Snowflake 전용
- Cortex Analyst NL2SQL + Semantic Model YAML — Snowflake 전용
- ML FORECAST 다중 시계열 118 series 학습 (`07:27`) — Snowflake 전용
- Streamlit in Snowflake + Git repository 배포 (`08:17`) — 데이터 외부 유출 없음
- Marketplace 4개 소스 직접 JOIN — Snowflake 데이터 공유 모델 전용

이 스택 중 3개 이상이 빠지면 프로젝트가 성립 불가. Agent를 범위에서 빼도 "Snowflake 필수"가 확립됨.

---

### AI 전문성 — 21/25점

#### A1 — Cortex 기능 적절 활용 (9/9점, +2)

**5개 Cortex 기능 동작 매트릭스 (Agent 제외)**

| 기능 | 용도 | 코드 증거 | 적절성 |
|------|------|----------|--------|
| AI_COMPLETE | 배치 프로필 생성 + Tab2 RAG 응답 + Tab3 이사 전망 | `03b:67,83`, `app.py:905,1170` | ✅ 자유형 생성·요약 |
| AI_CLASSIFY | 6카테고리 동네 유형 분류 | `04:13` | ✅ 사전 정의 카테고리 |
| AI_SENTIMENT | PROFILE_TEXT 감성 점수 → Tab1 카드 UI 표시 | `05:12`, `app.py:522-533` | ✅ 측면별 감성 |
| Cortex Search | Tab2 자연어 동네 검색 (REST 직접 호출) | `09:11`, `app.py:807-832` | ✅ 하이브리드 RAG |
| Cortex Analyst | Tab4 NL2SQL REST 직접 호출 + Semantic Model | `app.py:1278-1286`, `models/dongne_mbti.yaml` | ✅ YAML 기반 NL2SQL |

**rubric-ai.md:24 기준** — "5-6개 기능 모두 동작 + 각 기능이 적절한 용도" = **9점 조건 충족**.

**심사위원 시선**: Agent를 제외한 Cortex 전 영역이 용도에 맞게 동작한다. AI_SENTIMENT는 Tab1 카드 뱃지로, AI_CLASSIFY는 NEIGHBORHOOD_TYPE으로 실제 UI 가치를 낸다. AI 기능이 '알리바이'가 아닌 '가치'로 작동하는 증거가 분명.

---

#### A2 — AI를 가치 창출 구조로 활용 (7/8점)

**가치 창출 구조**
- **배치 저장 패턴**: `03b:67` AI_COMPLETE → DONG_PROFILES 저장 → `app.py:48 @st.cache_data(ttl=300)` → SELECT 조회만 ✅
- **멀티턴 대화**: `app.py:884-901` — `ARRAY_CONSTRUCT(OBJECT_CONSTRUCT)`로 히스토리를 CORTEX.COMPLETE messages에 주입 ✅
- **AI 결과 가시화**: `app.py:513-534` — NEIGHBORHOOD_TYPE 뱃지 + SENTIMENT_SCORE 색상 표시 ✅
- **Fallback 패턴**: `app.py:911-916` — MODEL_PRIMARY 실패 시 MODEL_FALLBACK 재시도 ✅
- **약점**: Dynamic Table 미사용. `rubric-ai.md:74` "AI 함수가 Dynamic Table 내 선언적 파이프라인"은 8점 조건.

**만점 받으려면**: Top Action #1 수행.

---

#### A3 — AI 모델 확장성 (5/8점)

**현재 상태**
- ✅ `app.py:15-16` — MODEL_PRIMARY/FALLBACK 상수 분리
- ✅ `models/dongne_mbti.yaml` — Semantic Model 테이블/관계 분리 (확장 시 YAML만 수정)
- ❌ `app.py:15` — `"mistral-large2"` 고정, `"auto"` 아님
- ❌ `03b_dong_profiles_create.sql:68,84` — 배치 파이프라인 `'snowflake-arctic'` 하드코딩
- ❌ `app.py:782` — `_SUPPORTED_SGG = {"서초구", "영등포구", "중구"}` 하드코딩

**심사위원 시선**: 상수 분리는 되었으나 'future-proof'의 핵심인 `"auto"`를 쓰지 않음. 2027년 새 모델 등장 시 코드 수정 필요.

**만점 받으려면**: Top Action #2, #3 수행 + `_SUPPORTED_SGG`를 `session.sql("SELECT DISTINCT SGG FROM ...")` 런타임 조회로 전환.

---

### 현실성 — 14/15점

#### R1 — 구현 완성도 (5/5점)

**4탭 완성 + Fallback 설계**
- Tab1: MBTI 카드 + 베프/라이벌 + 궁합 + 캐릭터 대화 + NEIGHBORHOOD_TYPE 뱃지 + SENTIMENT 라벨 (`app.py:462-773`)
- Tab2: Cortex Search + AI_COMPLETE 멀티턴 + SQL ILIKE 폴백 + 지원 범위 필터 (`app.py:923-1012`)
- Tab3: Altair 실거래 차트 + ML FORECAST 예측 + AI 이사 전망 (`app.py:1033-1190`)
- Tab4: Cortex Analyst NL2SQL + SQL/데이터 표시 + 예시 질문 5종 (`app.py:1195-1331`)
- SQL 체계: `sql/schema/01~10` + `sql/eda/00~05` 전량
- 배포: `08_streamlit_deploy.sql:17` Git integration

**심사위원 시선**: Fallback 설계까지 포함된 '운영 가능' 수준. 4탭 모두 동작.

---

#### R2 — 자원·비용 합리성 (4/5점)

**강점**
- ✅ XSMALL + AUTO_SUSPEND=60 (`dev-strategy.md:28-30`)
- ✅ 예산 배분표 $40 → $8/12/8/6/4 + $2 여유분 (`dev-strategy.md:34-42`)
- ✅ 배치 저장 → SELECT 조회 패턴 구현 (`03b/04/05` + `app.py:48 @st.cache_data`)
- ✅ `07_ml_forecast.sql:27` ON_ERROR:SKIP
- ✅ `09_cortex_search.sql:15` TARGET_LAG='1 day' 증분 인덱싱

**약점**
- ❌ `AI_COUNT_TOKENS` 사전 추정 쿼리 없음 (-0.5)
- ❌ 모델 선택 근거 문서화 없음 (-0.5)

**만점 받으려면**: Top Action #4.

---

#### R3 — 문제 해결의 논리성 (5/5점)

- `03_dong_mbti_result.sql:1-15` — 4축 피처 선정 근거 + 부호 방향 명시
- `docs/mbti-mapping-logic.md` — "왜 이 피처가 이 축인가" 논리 문서화
- ML FORECAST 학습 데이터 5년치 월별 시계열 (최소 1시즌 기준 통과)
- 측정 가능 목표: "16 MBTI 유형 전수 달성" (`project-plan.md:96`, `03:158` 검증 쿼리)
- 문제→기술 1:1 매핑: 분류(Classify)·감성(Sentiment)·NL2SQL(Analyst)·시계열(ML FORECAST)·텍스트 검색(Search)

---

## 총평

### 강점 3개 (Agent 제외 시에도 유지)

1. **4개 Marketplace cross-domain JOIN으로 파생 지표 창출 (S2 8/8)** — SPH·RICHGO·DataKnows·Subway를 `DISTRICT_CODE` 키로 결합, z-score 정규화, 부호 방향 설계까지. 이 한 축만으로 기술 트랙 인상 확보.

2. **Cortex 5개 기능 전수 동작 + UI 가시화 (A1 9/9)** — Complete·Classify·Sentiment·Search·Analyst 모두 용도에 맞게 사용. 특히 Tab1의 NEIGHBORHOOD_TYPE 뱃지와 Tab4 Analyst REST 직접 호출로 "AI가 실제 가치를 낸다"는 스토리가 명확.

3. **4탭 E2E 완성 + Fallback 3중 설계 (R1 5/5)** — Cortex Search 실패 시 SQL ILIKE, AI_COMPLETE 실패 시 Arctic 재시도, Analyst 에러 핸들링. 데모 가능한 운영 수준.

### 약점 3개 (즉시 수정 효과적)

1. **Dynamic Table 미사용 (S1 -2, A2 -1)** — AI_SENTIMENT/CLASSIFY 결과를 UPDATE 배치로만 반영. Dynamic Table 1개 신설로 선언적 파이프라인 전환 시 +3점 동시 확보.

2. **모델 `"auto"` 미사용 (A3 -1~2)** — `app.py:15` + `03b:68,84`에 특정 모델명 고정. 2027년 확장성 감점.

3. **AI_COUNT_TOKENS + 레퍼런스 부재 (R2 -0.5, C1/C2 -1)** — 비용 의식과 경쟁 차별점 주장이 있으나 '정량적 근거'가 한 단계 부족.

---

## 액션 플랜

### P0 (제출 전 필수 — 2026-04-12 마감 전)

- [ ] **[A3 +1]** `app.py:15` → `MODEL_PRIMARY = "auto"`, Tab2/Tab3 smoke test. ⏱ 5분
- [ ] **[A3 +0.5]** `03b_dong_profiles_create.sql:68,84` → `'auto'` 또는 SQL 변수. ⏱ 10분
- [ ] **[R1 재검증]** Snowflake 웹에서 `SHOW STREAMLITS`·`SHOW CORTEX SEARCH SERVICES` 실행해 배포 스크린샷 확보. ⏱ 10분

### P1 (여력 있을 때)

- [ ] **[S1 +1, A2 +1]** `sql/schema/11_dynamic_table_profiles.sql` 신설 — `DONG_PROFILES_ENRICHED`를 Dynamic Table로, `AI_SENTIMENT`를 SELECT 내장. ⏱ 40분
- [ ] **[R2 +0.5]** `sql/eda/06_token_cost_estimate.sql` 신설 — `AI_COUNT_TOKENS(MODEL_PRIMARY, sample_prompt)`로 Tab2 평균 비용 1건. ⏱ 20분
- [ ] **[C1 +0.5]** `project-plan.md:16` 학술·산업 레퍼런스 1개. ⏱ 15분
- [ ] **[C2 +0.5]** `project-plan.md:10` 사용자 페인포인트 조사 1줄. ⏱ 10분
- [ ] **[A3 +0.5]** `app.py:782` `_SUPPORTED_SGG` 런타임 조회 전환. ⏱ 15분

### 예상 점수 경로
- 현재(Agent 제외): **78/90**
- P0 전량: **79.5/90**
- P0 + P1 전량: **82~83/90**

---

## Agent 포함 평가 대비 차이 (투명성)

| 항목 | Agent 포함(75) | Agent 제외(78) | 차이 사유 |
|------|---------------|---------------|----------|
| A1 | 7/9 | 9/9 | Step 3 "앱에서 agent:run 미호출" 감점이 범위 제외로 소거. 5개 기능 전수 동작 조건 만족. |
| S3 | 7/8 | 8/8 | "Snowflake만 가능" 핵심 결정타가 Agent 오케스트레이션이었으나 범위 제외. 남은 5 Cortex + ML FORECAST + SiS + Marketplace로 전용성 확립. |
| 나머지 | 변동 없음 | 변동 없음 | — |

**주의**: 실제 심사가 Cortex Agent를 여전히 요구할 가능성은 있음. 이 평가는 "Trial 계정 399504 에러로 Agent 미배포"라는 현실 제약 하에서의 최선 시나리오.
