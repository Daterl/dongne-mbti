# Task Plan: 해커톤 점수 개선 스프린트 (Cortex Agent 제외)

## Goal
평가 68점 → 79점+ 달성. Cortex Agent 제외, 즉시 실행 가능한 항목으로 2026-04-12 마감 전 완료.

## 현재 점수 vs 목표
| 카테고리 | 현재 | 목표 | 개선 액션 |
|---------|------|------|---------|
| 창의성 (C1·C2·C3) | 17 | 21 | 차별점 문서화 + 정량 근거 |
| Snowflake 전문성 (S1·S2·S3) | 21 | 22 | 배포 검증 SQL |
| AI 전문성 (A1·A2·A3) | 17 | 21 | 모델 상수화 + AI 기능 가시화 |
| 현실성 (R1·R2·R3) | 13 | 14 | NEIGHBORHOOD_TYPE UI 노출 |
| **합계** | **68** | **78~79** | — |

---

## Phases

### Phase 1: 문서 개선 — 창의성 +4점 (30분)
- [x] 1-1. `docs/project-plan.md` — 직방·호갱노노 대비 차별점 명시 (C1 +2점)
- [x] 1-2. `docs/project-plan.md` — 정량 근거 추가: 이사 인구 통계 (C2 +2점)
- [x] 1-3. `docs/project-plan.md` — C3 기존 대비 개선점 정량 표현 (보너스)

### Phase 2: 코드 — 모델 상수화 (A3 +2점, 15분)
- [x] 2-1. `streamlit/app.py` — `MODEL_PRIMARY/MODEL_FALLBACK` 상수 선언 + 전체 치환 완료
- [x] 2-2. `streamlit/app.py` — FALLBACK 상수도 함께 선언 완료

### Phase 3: UI — AI 기능 가시화 (A1 +1점, R1 +1점, 1~2시간)
- [x] 3-1. Tab1 카드 — `NEIGHBORHOOD_TYPE` 뱃지 추가 (AI_CLASSIFY 결과 노출)
- [x] 3-2. Tab1 카드 — `SENTIMENT_SCORE` 감성 지수 표시 (AI_SENTIMENT 결과 노출)
- [x] 3-3. Tab2 — "Cortex Search 기반" 라벨 + 작동 방식 info박스 추가

### Phase 4: SQL 보완 — 비용/배포 검증 (R2 +0.5점, 30분)
- [x] 4-1. `sql/schema/00_verify.sql` 생성 — SHOW STREAMLITS, SHOW CORTEX SEARCH SERVICES
- [x] 4-2. AI_COUNT_TOKENS 비용 추정 쿼리 추가 (00_verify.sql:10~28)

### Phase 5: 검증 + 배포 준비
- [ ] 5-1. git push (코드 변경 반영)
- [ ] 5-2. CoCo에 `ALTER GIT REPOSITORY FETCH` 실행 후 SiS 재배포
- [ ] 5-3. 변경된 항목 점수 재산정 (목표 79점 확인)

---

## Key Decisions
- **Cortex Agent 제외**: Trial 계정 399504 에러. DDL은 유지, 앱 미호출 상태 유지.
- **모델 상수화 우선**: A3 +2점으로 ROI 최고. 코드 1줄 변경.
- **문서 개선 우선**: C1/C2 합산 +4점, 30분 작업으로 최대 효과.

## Errors Encountered
- (없음 — 진행 중)

## Status
**Phase 1 시작** — 문서 개선부터 진행.
