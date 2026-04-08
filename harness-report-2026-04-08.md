# Harness Engineering Audit — dongne-mbti

> 진단일: 2026-04-08 | 적합성: human-in-the-loop (사용자 명시 요청으로 전체 진단)

## 프로젝트 개요

- **스택**: Snowflake SQL + Streamlit + Cortex AI
- **파일 수**: 하네스 7파일 (718줄), docs 6파일
- **git**: 6 commits, main branch, 에이전트 커밋 0건

---

## 축 1: Context Engineering — L2

| 항목 | 결과 | 근거 |
|------|------|------|
| CLAUDE.md 존재 | ✅ | `.claude/CLAUDE.md` 115줄 |
| 에이전트 정의 | ✅ | 4개 (developer, data-analyst, reviewer, wiki-writer) |
| 스킬 정의 | ✅ | 2개 (report, checkpoint) |
| docs/ 포인터 | ✅ | 5개 (project-plan, data-sources, dev-strategy, query-examples, submission-checklist) |
| why/imperative 비율 | ✅ | 6 / (4+1) = 1.2 (≤3.0 기준 충족) |
| CLAUDE.md 커밋 횟수 | ❌ | 1회 (L4 기준: 5회+) |
| 서브폴더 계층 (nearest-wins) | ❌ | 단일 .claude/CLAUDE.md만 존재 |
| Progressive Disclosure | ❌ | references/ 디렉토리 없음, SKILL.md가 직접 모든 내용 포함 |
| ONBOARDING.md | ❌ | 미존재 |

**판정: L2** — CLAUDE.md + agents + skills 존재하지만, living document가 아니고 Progressive Disclosure 미적용.

**L3 조건**: docs/ 포인터 3개+ ✅, 강압/이유 비율 ≤3.0 ✅, 100줄 이하 ❌ (115줄, 미세 초과)
→ CLAUDE.md를 100줄 이내로 줄이면 L3 즉시 달성 가능

---

## 축 2: Architectural Constraints — L1

| 항목 | 결과 | 근거 |
|------|------|------|
| 린터 설정 | ❌ | .eslintrc, biome.json 등 없음 |
| CI 설정 | ❌ | .github/workflows/ 없음 |
| pre-commit hooks | ❌ | .husky/, .pre-commit-config.yaml 없음 |
| Claude Code hooks | ❌ | .claude/settings.json 없음 |
| 구조적 테스트 | ❌ | dependency-cruiser 등 없음 |
| 억제 코멘트 | N/A | 코드 파일 아직 없음 |
| Generator-Evaluator 분리 | ✅ | developer(Generator) ↔ reviewer(Evaluator) 명확 분리 |

**판정: L1** — 린터/CI/hooks 전무. Generator-Evaluator 분리는 달성했으나 기계적 강제 수단이 없음.

**L2 조건**: 린터 또는 CI 1개만 추가하면 달성
**L4 가산 경로**: Generator-Evaluator 분리 달성 → L3 도달 시 L4 가산 가능

---

## 축 3: Garbage Collection — L1

| 항목 | 결과 | 유형 |
|------|------|------|
| failFast 설정 | ❌ | Context |
| 출력 제한/필터링 | ❌ | Context |
| 토큰 최적화 (RTK 등) | ❌ (프로젝트 내) | Context |
| 정기 정리 자동화 | ❌ | Context |
| 학습 로그 로테이션 | N/A | Context |
| 포맷터 자동 강제 | ❌ | Self-Organization |
| 에이전트 코드 안정성 | N/A (에이전트 커밋 0건) | Evolutionary |

**판정: L1** — 출력 관리 메커니즘 전무.

> 참고: 글로벌 RTK 설정은 존재하지만 프로젝트 내 설정은 없음.

---

## 종합: L1

컨텍스트 엔지니어링(에이전트가 읽을 지식)은 L2로 양호한 출발이나, 가드레일(에이전트 실수 방지)과 GC(엔트로피 관리)가 전무하여 종합 L1.

## 즉각 액션 Top 3

### 1. `.claude/settings.json` 생성 — hooks로 가드레일 추가

SQL 파일 변경 시 기본 검증, 커밋 메시지 컨벤션 체크.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": ["test -f /Users/diego/dongne-mbti/sql/*.sql && echo 'SQL file change detected'"]
      }
    ]
  }
}
```

→ 축 2를 L1→L2로 올림

### 2. CLAUDE.md 규칙에 "왜" 보강

현재 imperative 6 vs why 4. 각 규칙에 이유를 한 줄씩 추가하면 L3 기준 충족.

예시:
- "LIMIT 10으로 테스트" → "LIMIT 10으로 테스트한다. 전체 실행 시 구 단위 25건에 ~$1 소비되므로 오류가 있으면 되돌릴 수 없기 때문이다."

### 3. skills/에 references/ 분리 준비

현재 SKILL.md가 91~113줄이라 당장 문제는 아니지만, 위키 템플릿·페이즈 정의 등을 references/로 분리하면 Progressive Disclosure 달성 → 축 1을 L2→L3로 올림.
