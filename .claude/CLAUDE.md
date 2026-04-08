# dongne-mbti 프로젝트

> Snowflake Hackathon 2026 Korea | 마감 4/12 | 크레딧 $40 | 2인 팀

서울 동네의 '성격'을 MBTI로 표현하는 Streamlit in Snowflake 앱.

## 하네스

**에이전트 (전문가 풀 — 필요 시 개별 호출):**

| 에이전트 | 역할 | 호출 시점 |
|---------|------|----------|
| developer | SQL, Streamlit, YAML, Cortex AI 코드 | 코드 작성 시 |
| data-analyst | EDA, 4축 피처 매핑, 통계 검증 | 데이터 분석 시 |
| reviewer | SQL 검증, 크레딧 추정, 프롬프트 점검 | Snowflake 실행 전 |
| wiki-writer | Wiki 기록 (로그, 체크포인트, 의사결정) | /report, /checkpoint 시 |

**스킬:** `/report` (일일 Wiki 로그), `/checkpoint` (페이즈 Wiki 체크포인트)

**규칙:** 단순 질문은 에이전트 없이 직접 응답. 모든 에이전트는 `model: "opus"`.

## 크레딧 세이프가드

- Cortex AI 호출 전 `LIMIT 10` 테스트 필수. 전체 실행(구 25건 ~$1, 동 400건 ~$10)은 테스트 후에만. # Why: Warehouse 1시간 방치 = $2, 전체 동 배치 = $10. $40 예산의 25~50% 소진.
- 결과는 테이블에 저장 → Streamlit에서 조회만 (배치 패턴). # Why: Cortex AI를 매 클릭마다 호출하면 데모 중 크레딧 고갈.
- SQL 실행 전 reviewer 에이전트 검증 권장. # Why: SQL 오류로 의미 없는 크레딧 소비 방지. 특히 JOIN 조건 누락 시 카테시안 곱 발생.
- Warehouse: `XSMALL`, `AUTO_SUSPEND=60`. 대형 사이즈 변경은 hooks가 차단. # Why: MEDIUM 이상은 시간당 $4~$16.

## 코드 분담

- **Claude Code (무료)**: SQL/Streamlit/YAML 작성, 문서화
- **Snowflake (크레딧)**: 실행, 검증, 앱 배포, 데모 촬영
- 구 단위(25개) MVP 먼저 → 여유 시 동 단위 확장. # Why: 구 단위 ~$1, 동 단위 ~$10+. MVP는 구 단위로 충분.

## Cortex AI 6개 기능 (심사 필수)

AI_CLASSIFY, AI_SENTIMENT, AI_COMPLETE, Cortex Search, Cortex Analyst, Cortex Agent — 모두 동작 확인 필수. 상세: `docs/submission-checklist.md`

## 데이터 소스

4종 Marketplace: RICHGO (실거래가), KOSIS_DEMO (인구), KOSIS_BIZ (사업체), NICE (상권). 스키마 553컬럼. 상세: `docs/data-sources.md`

## 참고

- `docs/project-plan.md` — 기획서 + 일정
- `docs/data-sources.md` — 스키마, JOIN 전략, MBTI 피처 매핑
- `docs/dev-strategy.md` — 크레딧 관리, 개발 흐름

---

**변경 이력:**

| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-04-08 | 초기 구성 | 전체 | 하네스 신규 구축 |
| 2026-04-08 | Why 보강 + 100줄 이내 리팩토링 | CLAUDE.md | 감사 L2→L3 개선 |
