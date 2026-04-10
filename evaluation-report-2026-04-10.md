# Snowflake Hackathon 기술 자가 평가 — dongne-mbti

> 평가일: 2026-04-10 | 마감: 2026-04-12 | 평가 기준: TECH TRACK 심사표 90점

---

## 요약 테이블

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Snowflake Hackathon 기술 자가 평가 — dongne-mbti / 2026-04-10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

카테고리              예상점수   만점   핵심 갭
─────────────────────────────────────────────────────────
창의성                17점      25점   project-plan.md: 차별점·정량 근거 미문서화
Snowflake 전문성      21점      25점   Dynamic Tables 미사용, Agent 미동작이 S3 약점
AI 전문성             17점      25점   app.py:384 — Agent 앱 미연동 (-3점 핵심)
현실성                13점      15점   배포 상태 미확인, AI_COUNT_TOKENS 미사용
─────────────────────────────────────────────────────────
기술 총점             68점      90점
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Top 5 즉각 액션 (점수 손실 영향순):**
1. [-3점] `app.py:384` — Cortex Search + AI_COMPLETE 직접 호출 → `agent:run` POST로 교체 (A1 핵심)
2. [-2점] `project-plan.md` — 직방·호갱노노 대비 명시적 차별점 + 정량 근거 1개 추가 (C1/C2)
3. [-2점] `app.py:388,601` — `'mistral-large2'` 하드코딩 → 상수/`'auto'` 분리 (A3)
4. [-1점] `app.py:Tab1` — SENTIMENT_SCORE·NEIGHBORHOOD_TYPE 카드 UI 시각화 (A1 가시화)
5. [-1점] SiS 배포 상태 확인 — `SHOW STREAMLITS` / `SHOW CORTEX SEARCH SERVICES` (R1)

---

## 항목별 세부 분석

### 창의성 — 17/25점

#### C1 — 차별화된 문제 정의·솔루션 (6/8점)

**현재 상태:** `project-plan.md:8` — "이사를 고민하는 사람이 동네의 '성격'을 직관적으로 이해하고..."라는 배경은 있음. MBTI 프레임워크로 동네를 표현하는 아이디어는 참신.

**심사위원 시선:** "직방·카카오 지도·호갱노노와의 차별점이 한 줄도 명시되지 않았다. '기존 서비스로 해결 안 되는 이유'가 없으면 C1 만점은 불가."

**만점 받으려면:** `project-plan.md` 배경에 "기존 서비스(직방/호갱노노)는 가격 정보만 제공하나, 동네 '성격'을 AI로 정의한 서비스는 없다" 한 문단 추가.

---

#### C2 — 문제 배경의 타당성 (5/9점)

**현재 상태:** 배경 서술 있으나 정량 근거 전무. "이사 인구", "탐색 시간" 등 수치 없음.

**심사위원 시선:** "문제는 공감되나 근거가 없다. '이사 고민하는 사람이 많다'는 주장 수준에 그친다."

**만점 받으려면:** 통계청 인구이동통계 1줄 인용. "연간 서울 전입 인구 약 60만 명(2023), 평균 탐색 기간 4.3개월" 등 정량 수치 1개.

---

#### C3 — 새로운 아이디어 또는 개선점 (6/8점)

**현재 상태:** 상권(SPH) + 부동산(RICHGO) + 역세권(DataKnows) → z-score 정규화 → MBTI 4축 판정이라는 Cross-domain 접근이 독창적. `03_dong_mbti_result.sql:19`에서 구현.

**심사위원 시선:** "기존 논문·서비스와의 정량 비교가 없다. 독창성은 있으나 '측정 가능한 개선'이 없다."

---

### Snowflake 전문성 — 21/25점

#### S1 — 플랫폼 기능 적절 활용·최적화 (7/9점)

**현재 상태:**
- `sql/schema/` 01~10 파일 체계화 ✅
- 사용 기능 8개+: `AI_COMPLETE`, `AI_CLASSIFY`, `AI_SENTIMENT`, `SNOWFLAKE.ML.FORECAST`, Cortex Search, Cortex Agent, SiS, Semantic Model
- `CREATE OR REPLACE AGENT` DDL 존재 (`06_cortex_agent.sql:7`) ✅
- `dev-strategy.md:28` — `WAREHOUSE_SIZE = 'XSMALL'`, `AUTO_SUSPEND = 60` 명시 ✅
- Dynamic Tables 미사용 (배치 UPDATE 방식)

---

#### S2 — 데이터 자산 혁신적 활용 (7/8점)

**현재 상태:**
- Marketplace 4개 소스: SPH(상권), RICHGO(부동산), DataKnows(역세권 AI), Telecom
- `03_dong_mbti_result.sql:21~54` — 4개 피처 테이블 JOIN으로 기존에 없던 MBTI 지표 생성 ✅
- `dk_jeonse_ratio`, `avg_subway_distance_m` 등 Cross-domain 결합으로 새 인사이트

---

#### S3 — Snowflake로만 가능한 해결책 (7/8점)

**현재 상태:**
- AI_CLASSIFY/SENTIMENT/COMPLETE가 SQL 파이프라인에 내장 ✅
- SiS 배포 (데이터 외부 유출 없음) ✅
- ML FORECAST Snowflake 전용 ✅
- Cortex Agent DDL만 있고 앱에서 실제 호출 안 됨 → "Snowflake 전용 핵심" 약점

---

### AI 전문성 — 17/25점

#### A1 — Cortex 6개 기능 적절 활용 (6/9점)

| 기능 | 코드 증거 | 상태 |
|------|----------|------|
| AI_COMPLETE | `03b:67,83` 프로필 생성 + `app.py:385,601` RAG 응답·이사 전망 | ✅ |
| AI_CLASSIFY | `04_dong_profiles_classify.sql:12` 6카테고리 동네 유형 | ✅ |
| AI_SENTIMENT | `05_dong_profiles_sentiment.sql:12` PROFILE_TEXT 감성 점수 | ✅ (형식적) |
| Cortex Search | `09_cortex_search.sql:11` DDL + `app.py:317` REST 호출 | ✅ |
| Cortex Analyst | `models/dongne_mbti.yaml` + `06_cortex_agent.sql:34` 등록 | ✅ |
| **Cortex Agent** | `06_cortex_agent.sql:7` DDL 완성, tools 양쪽 등록 | ⚠️ **app.py 미호출** |

**Agent 정적 4단계 검증:**
- Step 1 ✅: `06_cortex_agent.sql:23~37` — `tools: [search_dongne, query_dongne]` 양쪽 등록
- Step 2 ✅: `06_cortex_agent.sql:20` — Search/Analyst 라우팅 instructions 명시
- Step 3 ❌: `app.py:384` — `session.sql("SELECT SNOWFLAKE.CORTEX.COMPLETE(...)")` 직접 호출. `agent:run` POST 없음
- Step 4: `warehouse: "COMPUTE_WH"` ✅, `"orchestration": "auto"` ✅, budget 300초/20만 토큰 ✅

**심사위원 시선:** "Agent DDL은 완성도 높다. 그런데 앱 코드를 보면 실제로 Agent를 호출하지 않는다. Tab2는 Cortex Search + AI_COMPLETE 직접 연결이다. Agent 오케스트레이션이 없다."

---

#### A2 — AI를 가치 창출 구조로 활용 (6/8점)

**현재 상태:**
- `03b_dong_profiles_create.sql` — AI_COMPLETE 배치 → DONG_PROFILES 테이블 저장 ✅
- `app.py:49,56` — `@st.cache_data(ttl=300)` + SELECT 조회만 ✅
- Tab3 `app.py:587` — 버튼 클릭 시 실시간 AI_COMPLETE (사용자 선택형, 허용 가능)
- Dynamic Table 없이 단순 UPDATE 배치

---

#### A3 — AI 모델 확장성 (5/8점)

**현재 상태:**
- `06_cortex_agent.sql:5` — `"orchestration": "auto"` ✅
- `app.py:388` — `'mistral-large2'` **하드코딩** ❌
- `app.py:396` — 폴백 `'snowflake-arctic'` **하드코딩** ❌
- `03b:67,83` — `'snowflake-arctic'` **하드코딩** ❌
- `models/dongne_mbti.yaml` — Semantic Model 분리 ✅
- `app.py:281` — `_SUPPORTED_SGG = {"서초구", "영등포구", "중구"}` 하드코딩 (구 확장 시 코드 수정)

**만점 받으려면:** `app.py` 최상단에 `MODEL_NAME = "mistral-large2"` 상수 선언 또는 `"auto"` 변경 1줄.

---

### 현실성 — 13/15점

#### R1 — 구현 완성도 (4/5점)

**현재 상태:**
- Tab1·Tab2·Tab3 코드 완성 ✅
- SQL 01~10 전부 작성, Semantic Model YAML 완성 ✅
- NEIGHBORHOOD_TYPE·SENTIMENT_SCORE 컬럼이 DONG_PROFILES에 있으나 Tab1 UI에서 미노출
- SiS 배포 상태 미확인 (SiS UI 에러 이슈 있었음)

---

#### R2 — 자원·비용 합리성 (4/5점)

**현재 상태:**
- `dev-strategy.md:28~30` — XSMALL, AUTO_SUSPEND=60, 예산 배분 상세 ✅
- 배치 저장 패턴 구현 ✅
- `AI_COUNT_TOKENS` 미사용 ❌

---

#### R3 — 문제 해결의 논리성 (5/5점)

**현재 상태:**
- `03_dong_mbti_result.sql:3~14` — 4축 피처 선택 근거 상세 주석 ✅
- z-score 정규화 → MBTI 판정 파이프라인 논리 명확
- ML FORECAST 학습 데이터: RICHGO 2021~2026 약 5년 ✅ (최소 1시즌 이상)
- 16 MBTI 유형 전수 달성 목표 정량 측정 가능

---

## 총평

### 강점 3개
1. **Snowflake 전용성 높음** — AI_CLASSIFY·AI_SENTIMENT·AI_COMPLETE가 SQL 파이프라인에 내장, ML FORECAST, SiS 배포까지 Snowflake 안에서 완결.
2. **4개 Marketplace 데이터 Cross-domain JOIN** — SPH+RICHGO+DataKnows+Subway → z-score 정규화 → MBTI 4축이라는 새 지표 창출. S2 최강 항목.
3. **Cortex Agent DDL 완성도** — `warehouse`, `"auto"` 모델, `budget`, 라우팅 instructions, Search+Analyst 양쪽 tools 등록. 코드 품질 높음.

### 약점 3개 (즉시 수정 효과적)
1. **Agent 앱 미연동** (`app.py:384`) — A1에서 -2~3점. DDL 완성됐으나 Tab2가 실제로 Agent를 호출하지 않음.
2. **모델 하드코딩** (`app.py:388, 601`, `03b:67`) — A3에서 -2점. 상수 1개 선언으로 즉시 해결.
3. **창의성 문서 부재** — C1/C2에서 -4점. 기존 서비스 대비 차별점·정량 근거 부재.

---

## 액션 플랜

### P0 (제출 전 필수 — 4/12까지)
- [ ] `app.py:388,601` `'mistral-large2'` → `MODEL_NAME` 상수 분리 (30분)
- [ ] `project-plan.md` 직방 대비 차별점 + 정량 근거 1줄 추가 (30분)
- [ ] Tab1 카드에 `NEIGHBORHOOD_TYPE` 뱃지 표시 (1시간)
- [ ] `SHOW STREAMLITS` + `SHOW CORTEX SEARCH SERVICES` 확인

### P1 (여력 있을 때)
- [ ] Tab2 `_search_and_respond` → `agent:run` POST로 교체 (Cortex Agent runtime 동작 시)
- [ ] `AI_COUNT_TOKENS`로 사전 비용 추정 쿼리 추가
