# Task Plan: dongne-mbti 해커톤 마감 스프린트

## Goal
2026-04-12 마감 전까지 Cortex AI 6개 기능 전수 동작 + E2E 테스트 + 제출물 3종 완성

## 마감 타임라인
- **오늘 (4/9 오후)**: 플래닝 + 코드 준비 완료 (Claude Code)
- **CoCo 리셋 후 (4/9 저녁)**: 마이그레이션 + SiS 재배포 + E2E 테스트
- **4/10**: 버그 수정 + 데모 시나리오 작성
- **4/11**: UI 폴리싱 + 리허설
- **4/12**: 데모 영상 촬영 + PPT + ZIP 제출

---

## Phases

### Phase 1: 즉시 실행 (Claude Code — 지금)
- [x] Tab2 Cortex Agent 연동 코드 완성 (app.py `_run_agent`)
- [x] `warehouse: ""` → `"COMPUTE_WH"` 수정 (06_cortex_agent.sql)
- [x] Cortex Search DDL 신규 생성 (09_cortex_search.sql)
- [x] `mistral-large2` → `auto` 교체 (app.py)
- [x] 웨어하우스명 확인 (COMPUTE_WH)
- [x] **[#21 P0] DataKnows 피처 통합** (10_dataknows_features.sql + 03 업데이트)
  - [x] DONG_FEAT_SUBWAY — 역세권 피처 (S/N축 보강)
  - [x] DONG_FEAT_DK_PRICE — AI 시세 2026 (T/F·J/P축 업그레이드)
  - [x] 03_dong_mbti_result.sql — 신규 피처 반영 (v4)

### Phase 2: CoCo 리셋 후 (4/9 저녁 — Snowflake 실행)
- [ ] `SHOW WAREHOUSES` → WH명 확인
- [ ] 해커톤 계정 Marketplace 재구독 (SPH, RICHGO)
- [ ] `ALTER GIT REPOSITORY dongne_repo FETCH` (최신 코드 반영)
- [ ] SQL 01~09 순서대로 실행
  - [ ] 01_dongne_master.sql (DB + 마스터)
  - [ ] 02_dong_features.sql
  - [ ] 03_dong_mbti_result.sql
  - [ ] 04_dong_profiles_classify.sql (AI_CLASSIFY)
  - [ ] 05_dong_profiles_sentiment.sql (AI_SENTIMENT)
  - [ ] 06_cortex_agent.sql (Agent DDL, warehouse 수정 반영)
  - [ ] 07_ml_forecast.sql (ML FORECAST)
  - [ ] 08_streamlit_deploy.sql (SiS 배포)
  - [ ] 09_cortex_search.sql (Cortex Search, ~20분 인덱싱)
  - [ ] 10_dataknows_features.sql (DataKnows 역세권 + AI시세)

### Phase 3: E2E 테스트 (#18)
- [ ] Tab1 — 동네 카드 로드, 레이더 차트, 비교, 궁합 확인
- [ ] Tab2 — Agent 자연어 3턴 대화 (Search + Analyst 오케스트레이션 확인)
- [ ] Tab3 — ML FORECAST 차트 + AI 이사 전망 생성
- [ ] Cortex AI 6개 기능 전수 체크
  - [ ] AI_CLASSIFY (DONG_PROFILES.NEIGHBORHOOD_TYPE 존재)
  - [ ] AI_SENTIMENT (DONG_PROFILES.SENTIMENT_SCORE 존재)
  - [ ] AI_COMPLETE (Tab3 AI 전망 버튼)
  - [ ] Cortex Search (DONGNE_SEARCH 서비스 SHOW 확인)
  - [ ] Cortex Analyst (Tab2 Agent — query_dongne 호출 확인)
  - [ ] Cortex Agent (Tab2 3턴 대화 성공)

### Phase 4: 데모 시나리오 작성 (#19)
- [ ] 시나리오 1 (Tab1): 동네 비교 — 서초구 반포동 vs 영등포구 여의도동
- [ ] 시나리오 2 (Tab2): 자연어 3턴 대화 스크립트
- [ ] 시나리오 3 (Tab3): 이사 예보 — "지금 서초구 이사하면?"
- [ ] docs/demo-scenario.md 저장

### Phase 5: 최종 제출 (#20)
- [ ] PPT 슬라이드 구성 (문제→기술→결과→데모)
- [ ] 데모 영상 녹화 (QuickTime, 10분 이내)
- [ ] submission-checklist.md 전체 체크
- [ ] ZIP 패키징 (app.py + SQL + YAML + README)
- [ ] 제출 양식 작성 + 제출

---

## Key Decisions
- **마이그레이션 타이밍**: CoCo 리셋 후 (4/9 저녁) 일괄 실행
- **Tab2 전략**: Agent 연동 완성, Cortex Search DDL(09) 먼저 생성 필수
- **environment.yml**: 이미 수정 완료 (`plotly`만), git fetch 시 반영됨

## 현재 블로커
- CoCo 5시간 제한 (리셋 후 Phase 2 진행)
- 웨어하우스명 미확인 (COMPUTE_WH 가정, 다르면 3개 파일 수정 필요)
- Marketplace 재구독 필요 (SPH, RICHGO — 웹 UI 작업)

## Errors Encountered
- `warehouse: ""` 버그 → 수정 완료 (06_cortex_agent.sql)
- Tab2 Agent 미연동 → 수정 완료 (app.py `_run_agent`)
- Cortex Search DDL 없음 → 생성 완료 (09_cortex_search.sql)

## Status
**Phase 1 완료** — CoCo 리셋 대기 중. Phase 2 (마이그레이션) 준비 완료.
