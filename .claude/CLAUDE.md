# dongne-mbti 프로젝트

> Snowflake Hackathon 2026 Korea | 마감 4/12 | 크레딧 $40 | 2인 팀

서울 핵심 3구(서초·영등포·중) ~55개 동의 '성격'을 MBTI로 표현하는 Streamlit in Snowflake 앱.

## 하네스

**에이전트 (전문가 풀 — 필요 시 서브 에이전트로 호출):**

| 에이전트 | 역할 | 호출 시점 |
|---------|------|----------|
| developer | SQL, Streamlit, YAML, Cortex AI 코드 | 코드 작성 시 |
| data-analyst | EDA, 4축 피처 매핑, 통계 검증 | 데이터 분석 시 |
| reviewer | SQL 검증, 크레딧 추정, 프롬프트 점검 | Snowflake 실행 전 |
| wiki-writer | Wiki 기록 (로그, 체크포인트, 의사결정) | /report, /checkpoint 시 |

**스킬:** `/report` (일일 Wiki 로그), `/checkpoint` (페이즈 Wiki 체크포인트)

**규칙:** 단순 질문은 에이전트 없이 직접 응답. 모든 에이전트는 `model: "opus"`.

## 3구 55동 피봇 (2026-04-08 확정)

- **스코프**: 서초구, 영등포구, 중구 ~55개 동 딥다이브. Why: SPH+RICHGO가 3구만 커버. 25구 시도 시 22개 구 NULL.
- **데이터**: SPH(상권), RICHGO(실거래가+인구), Telecom V01/V05(구 단위 공유)
- **MBTI 4축**: E/I(SPH 활동성), S/N(SPH 라이프스타일), T/F(SPH+RICHGO 경제), J/P(RICHGO 변동성)
- **목표**: ~55동으로 16 MBTI 유형 전수 달성

## 크레딧 세이프가드

- Cortex AI 호출 전 `LIMIT 10` 테스트 필수. 전체 실행(3구 55동 ~$2-3)은 테스트 후에만. Why: $40 예산, Warehouse 1시간 방치 = $2.
- 결과는 테이블에 저장 → Streamlit에서 조회만 (배치 패턴). Why: 매 클릭마다 AI 호출 시 데모 중 크레딧 고갈.
- SQL 실행 전 reviewer 에이전트 검증 권장. Why: JOIN 조건 누락 → 카테시안 곱 → 크레딧 낭비.
- Warehouse: `XSMALL`, `AUTO_SUSPEND=60`. Why: MEDIUM 이상은 시간당 $4~$16.

## 코드 분담

- **Claude Code (무료)**: SQL/Streamlit/YAML 작성, 문서화
- **CoCo (Cortex Code CLI)**: Snowflake 실행, 검증
- **Snowflake**: 앱 배포, 데모 촬영

## Cortex AI 6개 기능 (심사 필수)

AI_CLASSIFY, AI_SENTIMENT, AI_COMPLETE, Cortex Search, Cortex Analyst, Cortex Agent — 모두 동작 확인 필수. 상세: `docs/submission-checklist.md`

## 데이터 소스

- **SPH**: 상권 데이터 (3구 동별 업종 분포, 유동인구)
- **RICHGO**: 실거래가 + 인구통계 (3구 매매/전세, 연령별 인구)
- **Telecom**: V01(월별 계약), V05(신규설치) — 구 단위만, 동 내 공유
- 상세: `docs/data-sources.md`

## 디렉토리 구조

```
.claude/
├── agents/
│   ├── developer.md
│   ├── data-analyst.md
│   ├── reviewer.md
│   └── wiki-writer.md
└── skills/
    ├── report/
    │   ├── SKILL.md
    │   └── references/daily-log-template.md
    └── checkpoint/
        ├── SKILL.md
        └── references/checkpoint-template.md
```

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
| 2026-04-08 | 3구 55동 피봇 반영 + 에이전트 파일 동기화 | 전체 | 25구→3구 피봇, 에이전트 정의 현행화 |
