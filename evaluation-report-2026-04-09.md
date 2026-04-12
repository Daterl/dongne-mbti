# 동네 MBTI — Snowflake Hackathon 기술 자가 평가 리포트

> 평가일: 2026-04-09 | 스킬: daterl:snowflake-hackathon-tech-evaluator v1.1.0
> 평가 범위: TECH TRACK 기술 4개 카테고리 (90점 만점)

---

## 요약 테이블

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Snowflake Hackathon 기술 자가 평가 — 동네 MBTI / 2026-04-09
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

카테고리              예상점수   만점   핵심 갭 (파일 인용)
─────────────────────────────────────────────────────────
창의성                17점      25점   project-plan.md — 문제 배경 정량 데이터 없음
Snowflake 전문성      21점      25점   Cortex Search DDL 미존재, Telecom 동 단위 미활용
AI 전문성             16점      25점   warehouse:"" 버그, Tab2 Agent 미연동, 모델 하드코딩
현실성                11점      15점   warehouse:"" 즉시 에러, Tab3 온디맨드 AI 호출
─────────────────────────────────────────────────────────
기술 총점             65점      90점

🎯 Top 5 즉각 액션 (점수 손실 영향순):
1. [P0·-4점] 06_cortex_agent.sql:44,52 — warehouse:"" → COMPUTE_WH 입력
2. [P0·-3점] sql/schema/ — CREATE CORTEX SEARCH SERVICE DDL 파일 없음
3. [P0·-2점] app.py:317-365 — Tab2 Agent 미연동, SQL ILIKE 폴백만 사용
4. [P1·-2점] app.py:355,499 — 'mistral-large2' 하드코딩 → "auto" 교체
5. [P1·-1점] project-plan.md:8 — 문제 배경 정량 데이터 없음
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 카테고리별 세부 분석

### 창의성 — 17/25점

| ID | 점수 | 근거 |
|----|------|------|
| C1 | 6/8 | README.md:9 — MBTI 프레임 독창적. "기존 서비스 X 한계 → Z로 해결" 명시 없음 |
| C2 | 5/9 | project-plan.md:8 — 배경 서술 있으나 정량 근거 없음 (이사 인구 수, 탐색 시간 등) |
| C3 | 6/8 | models/dongne_mbti.yaml — cross-domain JOIN으로 4축 생성. 정량 비교 없음 |

**C1 만점 받으려면**: "기존 직방·부동산114는 수치만 제공, 동네 '성격'을 직관적 언어로 표현 못함 → MBTI로 해결" 1문단 추가

**C2 만점 받으려면**: "연간 서울 이사 인구 XXX만 명, 평균 동네 탐색 시간 X시간" 정량 근거 1-2개 추가

---

### Snowflake 전문성 — 21/25점

| ID | 점수 | 근거 |
|----|------|------|
| S1 | 7/9 | 7개 기능 사용. XSMALL WH + AUTO_SUSPEND=60 ✅. Cortex Search DDL ❌. Dynamic Tables 미사용 |
| S2 | 7/8 | SPH × RICHGO cross-domain JOIN ✅. Telecom 구 단위만 (동 단위 미통합) |
| S3 | 7/8 | AISQL 파이프라인 내장 ✅. app.py:354 Tab2 CORTEX.COMPLETE 직접 호출 (Agent 우회) |

**기술 적합성 체크 (CoCo 스킬 대응):**
| CoCo 스킬 | Snowflake 기능 | 사용 여부 |
|----------|--------------|---------|
| cortex-ai-functions | AI_CLASSIFY, AI_SENTIMENT, AI_COMPLETE | ✅ |
| machine-learning | ML FORECAST | ✅ |
| cost-intelligence | AI_COUNT_TOKENS, COST_HISTORY | ❌ |
| data-quality | DMF | ❌ |
| lineage | OBJECT_DEPENDENCIES | ❌ (data-guardian 에이전트 정의만 있음) |

---

### AI 전문성 — 16/25점

| ID | 점수 | 근거 |
|----|------|------|
| A1 | 5/9 | Cortex Search DDL 없음, Agent warehouse:"" 버그, Tab2 Agent 미연동 |
| A2 | 6/8 | 배치 패턴 구현 ✅. app.py:497 Tab3 온디맨드 AI 호출 ❌ |
| A3 | 5/8 | Agent "auto" ✅. app.py:355,499 mistral-large2 하드코딩 ❌ |

**Cortex Agent 정적 코드 검증:**
| 단계 | 결과 | 근거 |
|------|------|------|
| Step 1: DDL tools: 배열 | ✅ | 06_cortex_agent.sql:23-37 — search_dongne + query_dongne 등록 |
| Step 2: Orchestration 라우팅 | ✅ | 06_cortex_agent.sql:20 — 도구 선택 로직 명시 |
| Step 3: 앱 호출 방식 | ❌ | app.py:354 — CORTEX.COMPLETE 직접 호출, /agent:run 없음 |
| Step 4: warehouse 필드 | ❌ | 06_cortex_agent.sql:44,52 — "" (빈 문자열, 런타임 에러) |

**AI_SENTIMENT 용도 적합성 주의**: 05_dong_profiles_sentiment.sql:12 — AI가 생성한 PROFILE_TEXT에 감성 분석 적용. 실제 리뷰 없이 AI→AI 순환 구조로 심사위원 의문 제기 가능.

---

### 현실성 — 11/15점

| ID | 점수 | 근거 |
|----|------|------|
| R1 | 3/5 | Tab1/3 동작 ✅. Tab2 Agent 미연동 ⚠️. warehouse:"" 런타임 에러 ❌ |
| R2 | 4/5 | 배치 패턴 + XSMALL + AUTO_SUSPEND ✅. AI_COUNT_TOKENS 없음, Tab3 온디맨드 ❌ |
| R3 | 4/5 | ML FORECAST 5년 데이터 ✅. AI_SENTIMENT 순환 구조 ⚠️ |

---

## 강점 / 약점 / 액션

### 강점 3개
1. **데이터 파이프라인 완성도** — SPH×RICHGO cross-domain JOIN → MBTI 4축. models/dongne_mbti.yaml 7개 verified_queries
2. **비용 관리 설계** — dev-strategy.md 배치 패턴 + XSMALL + AUTO_SUSPEND=60
3. **ML FORECAST 데이터 기반** — 5년 실거래가 데이터, 90% 신뢰구간 밴드 시각화 완성

### 약점 3개
1. `warehouse: ""` P0 버그 — Agent 전혀 실행 불가 (1분 수정으로 +2점)
2. Cortex Search DDL 없음 — Agent가 참조하는 서비스 미존재 (+2점)
3. Tab 2 Agent 미연동 — 핵심 기능인 "자연어 찾기"가 키워드 SQL 수준

### P0 (제출 전 필수)
- [ ] `sql/schema/06_cortex_agent.sql:44,52` — `"warehouse": ""` → `"warehouse": "COMPUTE_WH"`
- [ ] `sql/schema/09_cortex_search.sql` 신규 생성 — `CREATE CORTEX SEARCH SERVICE DONGNE_SEARCH`
- [ ] `streamlit/app.py:317-365` — Tab2 Agent endpoint 연동 또는 Cortex Search 직접 호출

### P1 (여력 있을 때)
- [ ] `streamlit/app.py:355,499` — `'mistral-large2'` → `'auto'` 교체 (A3 +2점)
- [ ] `docs/project-plan.md:8` — 문제 배경 정량 데이터 1-2개 추가 (C2 +2점)
- [ ] Tab3 AI 전망 — 배치 저장 패턴으로 전환 (R2 최적화)
