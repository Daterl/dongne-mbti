# dongne-mbti 프로젝트

> Snowflake Hackathon 2026 Korea | 동네 MBTI — AI로 읽는 동네 성격과 이사 타이밍
> 마감: 2026-04-12 (토) | 크레딧: $40 | 2인 팀

## 프로젝트 개요

서울 동네의 '성격'을 MBTI로 표현하고, 자연어로 맞춤 동네를 찾고, 이사 타이밍을 판단하는 Streamlit in Snowflake 앱.

---

## 하네스: 동네 MBTI 개발

**목표:** Snowflake Cortex AI 6개 기능을 활용한 동네 MBTI 앱을 $40 크레딧 내에서 개발하고, 모든 과정을 GitHub Wiki에 기록한다.

**에이전트 팀:**

| 에이전트 | 역할 |
|---------|------|
| developer | SQL, Streamlit, Semantic Model YAML, Cortex AI 파이프라인 개발 |
| data-analyst | EDA, MBTI 4축 피처 매핑, 데이터 품질 분석, 통계 검증 |
| reviewer | SQL 사전 검증, 크레딧 비용 추정, Cortex AI 프롬프트 점검 |
| wiki-writer | GitHub Wiki 페이지 생성/갱신 (일일 로그, 체크포인트, 의사결정) |

**스킬:**

| 스킬 | 용도 | 사용 에이전트 |
|------|------|-------------|
| /report | 일일 개발 리포트 → Wiki Daily Log | wiki-writer |
| /checkpoint | 페이즈 완료 체크포인트 → Wiki | wiki-writer |

**실행 규칙:**
- 에이전트는 전문가 풀 패턴으로 **필요 시 개별 호출**한다 (상시 팀 아님)
- SQL/Streamlit/YAML 코드 작성 시 → `developer` 에이전트 호출
- 데이터 탐색/분석/피처 매핑 시 → `data-analyst` 에이전트 호출
- Snowflake 실행 전 SQL 검증 시 → `reviewer` 에이전트 호출
- 티켓 완료/하루 마무리 시 → `/report` 스킬 (wiki-writer 호출)
- 페이즈 완료 시 → `/checkpoint` 스킬 (wiki-writer 호출)
- 단순 질문/확인은 에이전트 없이 직접 응답
- 모든 에이전트는 `model: "opus"` 사용

**디렉토리 구조:**

```
.claude/
├── agents/
│   ├── developer.md
│   ├── data-analyst.md
│   ├── reviewer.md
│   └── wiki-writer.md
├── skills/
│   ├── report/
│   │   └── SKILL.md
│   └── checkpoint/
│       └── SKILL.md
└── CLAUDE.md
```

---

## 개발 규칙

### Snowflake 크레딧 절약
- Warehouse: `XSMALL`, `AUTO_SUSPEND=60`
- Cortex AI 호출 전 반드시 `LIMIT 10`으로 테스트
- 결과는 테이블에 저장 → 이후 조회만 (배치 패턴)
- **SQL 실행 전 reviewer 에이전트로 검증 권장**

### 코드 작성 분담
- **Claude Code (무료)**: SQL 작성, Streamlit 코드, Semantic Model YAML, 문서화
- **Snowflake (크레딧)**: SQL 실행, 검증, 앱 배포, 데모 촬영

### Cortex AI 6개 기능 (모두 동작 필수)
1. `AI_CLASSIFY` — MBTI 4축 분류
2. `AI_SENTIMENT` — 동네 프로필 감성 분석
3. `AI_COMPLETE` — 성격 요약 + 이사 전망
4. `Cortex Search` — 동네 프로필 하이브리드 검색
5. `Cortex Analyst` — 자연어 → SQL (Semantic Model)
6. `Cortex Agent` — Search + Analyst 오케스트레이션

### 분석 단위
- **기본**: 서울 구 단위 (~25개, ~$1)
- **확장**: 서울 동 단위 (~400+개, ~$10+) — 여유 시만

### 위키 운영
- 티켓 완료 시 `/report`로 위키 기록
- 페이즈 완료 시 `/checkpoint`로 체크포인트 기록
- Wiki 리포: `https://github.com/Daterl/dongne-mbti.wiki.git`

---

## 데이터 소스 (Marketplace 4종)

| DB | 내용 |
|----|------|
| RICHGO_DATA_REAL_PRICE | 리치고 실거래가 (2021~2026) |
| KOSIS_DEMOGRAPHIC | 통계청 인구·가구 |
| KOSIS_BUSINESS | 사업체 통계 |
| NICE_COMMERCIAL | 나이스 상권 분석 |

## 참고 문서

- `docs/project-plan.md` — 기획서 + 수정 일정
- `docs/data-sources.md` — 스키마 553컬럼, JOIN 전략, MBTI 피처 매핑
- `docs/dev-strategy.md` — 크레딧 관리, 개발 흐름
- `docs/query-examples.md` — Cortex Agent 자연어 질의 22개 예시
- `docs/submission-checklist.md` — 제출 체크리스트

---

**변경 이력:**

| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-04-08 | 초기 구성 | 전체 | 하네스 신규 구축 |
