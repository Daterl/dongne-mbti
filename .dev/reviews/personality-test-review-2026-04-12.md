# Engineering Plan Review: 성향 테스트 탭 (기승전결)

**Date**: 2026-04-12
**Reviewer**: Claude (plan-eng-review)
**Verdict**: READY

---

## A. Scope & Boundaries

### Q1. What exactly changes?
**Confidence**: HIGH
- `streamlit/app.py` (1,340줄): 라인 458의 `st.tabs()` 호출 수정 (4탭→5탭), 새 `tab0` 블록 ~300줄 추가
- `streamlit/questions.py` (271줄): `SCORE_SCALE_FACTOR`, `reset_quiz_state()` 이미 추가 완료
- `streamlit/app.py`의 `st.experimental_rerun()` 6곳 → `st.rerun()` 교체 완료 (라인 963, 1005, 1010, 1238, 1335, 1340)

### Q2. What explicitly does NOT change?
**Confidence**: HIGH
- `streamlit/animals.py` — 기존 16 MBTI 동물 이미지 그대로 재사용
- `models/dongne_mbti.yaml` — Cortex Analyst Semantic Model 변경 없음
- `sql/schema/` — 모든 SQL 파이프라인 변경 없음, 신규 테이블 없음
- Snowflake 데이터: 읽기 전용 (DONG_PROFILES, DONG_MBTI_RESULT, PRICE_FORECAST_RESULT)
- 기존 tab1~tab4의 로직 — 변수명 변경만 (tab1→tab1, 위치 유지)

### Q3. Are there scope creep risks?
**Confidence**: HIGH
- **낮음.** 새 탭은 기존 데이터와 함수를 읽기만 함. 기존 `load_profiles()`, `load_mbti_result()`, `load_forecast()` 캐시 함수를 공유하지만 수정하지 않음.
- 유일한 리스크: CSS 클래스 이름 충돌 (새 `.quiz-*` 클래스가 기존 클래스와 겹칠 가능성) → 네임스페이스 prefix로 해결.

### Q4. Is the change reversible via git revert?
**Confidence**: HIGH
- 완전히 reversible. 데이터 변경 없음 (읽기 전용). `git revert`으로 app.py + questions.py 원복 가능.
- 단, `st.experimental_rerun()` → `st.rerun()` 교체는 독립적 개선이므로 revert하면 deprecated 함수로 돌아감. 이 교체는 별도 커밋으로 분리하는 것이 좋음.

---

## B. Data Safety

### Q5. What data operations does this involve?
**Confidence**: HIGH
- **READ only**: DONG_PROFILES, DONG_MBTI_RESULT, PRICE_FORECAST_RESULT, RICHGO 시세
- **AI_COMPLETE (실시간)**: 5-6회 호출 — 읽기+생성, 저장 없음
- **Cortex Search (실시간)**: 1회 조회 — 읽기만
- **DELETE/WRITE/SCHEMA_CHANGE**: 없음

### Q6. What happens if the operation fails midway?
**Confidence**: HIGH
- 퀴즈 응답: `session_state`에만 저장, 실패 시 사라짐 (의도된 동작)
- AI 호출 실패: 3단계 폴백 체인 (llama3.3-70b → snowflake-arctic → 정적 텍스트)
- 부분 렌더링: Phase A(DNA) 성공 + Phase B(추천) 실패 시 DNA 결과는 보이고 추천만 에러 메시지. 데이터 오염 불가.

### Q7. Is there a rollback plan for data changes?
**Confidence**: HIGH
- 해당 없음. 데이터 변경이 없으므로 롤백 불필요.

### Q8. What's the blast radius?
**Confidence**: HIGH
- **최소.** 최악의 경우: AI_COMPLETE 전체 실패 → 정적 텍스트 폴백으로 결과 표시. 사용자 경험 저하뿐, 데이터 손상 없음.
- 크레딧 영향: 세션당 ~$0.0012, 무한루프 없음 (time.sleep(2) 후 단 1회 st.rerun()).
- 기존 탭: 변수명(tab1~tab4) 유지되므로 기존 기능에 영향 없음. `st.rerun()` 교체는 Streamlit 호환성 개선.

---

## C. Dependencies & Integration

### Q9. What upstream systems feed into the affected area?
**Confidence**: HIGH
- `DONG_PROFILES` (118행): AI_COMPLETE로 배치 생성된 프로필, CHARACTER_SUMMARY
- `DONG_MBTI_RESULT` (118행): z-score 정규화된 4축 점수
- `PRICE_FORECAST_RESULT`: ML FORECAST 결과 (3개월 예측)
- `RICHGO` 실거래가: 시세 차트용 시계열 데이터
- 모두 이미 존재하고 변하지 않는 읽기 전용 테이블.

### Q10. What downstream systems consume from the affected area?
**Confidence**: HIGH
- 없음. 새 탭은 결과를 화면에만 렌더링하고 테이블에 저장하지 않음.

### Q11. Are there shared state changes?
**Confidence**: HIGH
- `session_state` 키 추가: `quiz_step`, `quiz_answers`, `quiz_completed`, `quiz_user_scores`, `quiz_user_mbti`, `quiz_matches`, `quiz_dna_text`, `quiz_rec_texts`
- 기존 키(`messages`, `_pending`, `analyst_history`, `_analyst_pending`)와 충돌 없음 (모두 `quiz_` prefix).
- CSS: 기존 `<style>` 블록에 `.quiz-*` 클래스 추가. 기존 클래스명과 겹치지 않음.

### Q12. What timing/ordering constraints exist?
**Confidence**: HIGH
- 없음. 새 탭은 독립적. 배포 순서 제약 없음.
- Snowflake 쪽: Git repo FETCH → SiS 앱 자동 반영. 추가 DDL 불필요.

---

## D. Testing & Verification

### Q13. How will correctness be verified?
**Confidence**: MEDIUM
- **수동 검증**: Snowsight에서 DONGNE_MBTI_DEV 앱 열고 8개 질문 완료 → 결과 확인
- **DoD 체크리스트**: 인트로 → 8문제 → 분석 → MBTI 카드 + DNA + TOP 3 + 시세 → 전체 렌더링
- **단위 테스트**: questions.py의 `compute_user_scores()`, `match_neighborhoods()` 등은 순수 함수이므로 로컬에서 pytest 가능 (현재 미설정)
- 자동화된 테스트는 없지만, 해커톤 컨텍스트에서는 수동 검증으로 충분.

### Q14. What edge cases need specific attention?
**Confidence**: HIGH
1. **8개 모두 같은 위치 선택** (예: 전부 A) → 특정 축 과편향 → 매칭 결과가 극소수 동네에 집중. `compute_match_pct()`가 0% 미만이 되지 않도록 `max(0, ...)` 처리 완료.
2. **AI_COMPLETE 전체 실패** → 3단계 폴백 체인. 최종 정적 텍스트는 `generate_user_dna_text()`로 보장.
3. **DONG_PROFILES 빈 DataFrame** → `match_neighborhoods()`가 빈 리스트 반환 → 결과 화면에서 분기 처리 필요 (구현 시 `if not matches:` 체크).
4. **time.sleep(2) 후 st.rerun()** → 무한루프 아닌지 확인: `quiz_step`이 9→10으로 변경되므로 1회만 실행.

### Q15. How will production behavior be monitored post-deploy?
**Confidence**: MEDIUM
- **해커톤 컨텍스트**: 프로덕션 모니터링 해당 없음. 데모 중 수동 확인.
- AI 호출 비용: `SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY`로 크레딧 소비 확인 가능.

### Q16. Is there a canary/gradual rollout strategy?
**Confidence**: HIGH
- **dev 브랜치 분리**: `DONGNE_MBTI_DEV` 앱으로 별도 배포. main의 `DONGNE_MBTI_APP`은 건드리지 않음.
- 검증 완료 후 dev → main 머지로 프로덕션 배포.

---

## E. Implementation Strategy

### Q17. What's the migration path?
**Confidence**: HIGH
- **단일 PR**: app.py에 ~300줄 추가 (새 탭). Big bang이지만 리스크 낮음 — 기존 코드 수정 최소 (탭 변수 추가만).
- questions.py 수정은 이미 완료.
- 순서: 코드 작성 → dev push → FETCH → DEV 앱 테스트 → main 머지.

### Q18. What's the point of no return?
**Confidence**: HIGH
- **없음.** 데이터 변경 없음. 어느 시점에서든 `git revert` 가능.

### Q19. What are the prerequisites?
**Confidence**: HIGH
- [x] dev 브랜치 생성 — 완료
- [x] questions.py 스코어링 로직 — 완료
- [x] st.experimental_rerun() 교체 — 완료
- [x] .gitignore 설정 — 완료
- [ ] Snowsight에서 `DONGNE_MBTI_DEV` 앱 생성 — **사용자가 SQL 실행 필요**
- [ ] Git auto-fetch TASK 생성 — **사용자가 SQL 실행 필요** (선택)

### Q20. What's the worst-case scenario and mitigation?
**Confidence**: HIGH
- **최악**: app.py 수정 시 구문 오류 → SiS 앱 전체 로드 실패 (빈 화면).
  - **완화**: dev 브랜치에서만 작업, main 불변. DEV 앱만 영향.
  - **복구**: `git revert` 후 `FETCH`.
- **차악**: AI_COMPLETE 5-6회 연속 호출로 30초+ 로딩 → 사용자 이탈.
  - **완화**: 점진적 렌더링 (Phase A 먼저 표시 → Phase B 로딩).
- **크레딧 리스크**: 무한루프로 AI 호출 반복 → 크레딧 고갈.
  - **완화**: `quiz_step` 상태 기계가 단방향 (0→10). time.sleep 후 st.rerun은 1회만. 무한루프 구조적으로 불가.

---

## Verdict: READY

**Confidence Distribution**: HIGH: 17/20 · MEDIUM: 3/20 · LOW: 0/20

**Rationale**: 데이터 변경이 없는 읽기 전용 UI 추가이므로 리스크가 구조적으로 낮습니다. dev 브랜치 분리로 기존 앱에 영향 없음. 스코어링 로직과 폴백 체인이 이미 구현되어 있고, 모든 20개 질문에 대해 근거가 확인되었습니다.

### Action Items (구현 전 확인)

| # | Question | Issue | Priority |
|---|----------|-------|----------|
| 1 | Q19 | Snowsight에서 DEV 앱 생성 SQL 실행 필요 (사용자) | HIGH |
| 2 | Q14 | 빈 DataFrame 방어 코드 (`if not matches:`) 구현 시 추가 | MEDIUM |
| 3 | Q4 | `st.rerun()` 교체를 별도 커밋으로 분리 권장 | LOW |

---

## Metadata

- **Plan source**: `docs/plans/personality-test-spec.md`
- **Files researched**: `streamlit/app.py` (1340줄), `streamlit/questions.py` (271줄), `streamlit/animals.py`, `streamlit/environment.yml`, `models/dongne_mbti.yaml`, `sql/schema/03_dong_mbti_result.sql`
- **Review source**: `specs/personality-test-review.md`
- **Codebase queries**: st.tabs 위치, session_state 키 목록, import 목록, cache 함수 목록, Snowflake 테이블 참조, Cortex AI 호출 위치
