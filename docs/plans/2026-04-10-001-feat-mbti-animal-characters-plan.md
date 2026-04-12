---
title: "feat: MBTI 16종 동물 캐릭터 SVG 제작 및 카드 통합"
type: feat
status: active
date: 2026-04-10
origin: docs/brainstorms/2026-04-10-mbti-animal-characters-requirements.md
---

# feat: MBTI 16종 동물 캐릭터 SVG 제작 및 카드 통합

## Overview

MBTI 16종 각각에 대응하는 동물 캐릭터 SVG를 인라인으로 제작하고, 탭1 MBTI 카드에 통합한다. 바이럴 공유 임팩트를 높이기 위한 시각적 아이덴티티 구축.

## Problem Frame

현재 MBTI 카드는 텍스트(MBTI 타입 + 4축 칩 + CHARACTER_SUMMARY)로만 구성되어 있어 인스타그램 공유 시 시각적 매력이 부족하다. 동물 캐릭터를 추가해 MBTI별 아이덴티티를 부여한다. (see origin: docs/brainstorms/2026-04-10-mbti-animal-characters-requirements.md)

## Requirements Trace

- R1. MBTI 16종 각각에 대응하는 동물 캐릭터 SVG를 인라인으로 제작
- R2. 각 동물은 4축 데이터 특성을 반영하는 소품/특징 보유
- R3. SVG는 플랫/미니멀 스타일, MBTI_COLORS 팔레트 색상 사용
- R4. `MBTI_ANIMALS` 딕셔너리로 SVG 코드 관리 (origin은 app.py 명시 → 파일 크기 문제로 `animals.py`로 분리 결정, Key Decisions 참조)
- R5. 탭1 MBTI 카드에 캐릭터 표시
- R6. `st.markdown(unsafe_allow_html=True)`로 렌더링 (SiS 호환)

## Scope Boundaries

- 55개 동네별 개별 캐릭터 없음 (MBTI 16종 기준)
- 애니메이션/인터랙션 없음
- 인스타그램 카드 별도 export 기능 제외

## Context & Research

### Relevant Code and Patterns

- `streamlit/app.py:30-36` — `MBTI_COLORS` 딕셔너리: 16종 MBTI별 hex 색상 상수. 동일 패턴으로 `MBTI_ANIMALS` 딕셔너리 구성
- `streamlit/app.py:172-185` — MBTI 카드 HTML: `<div class="mbti-card">` 안에 타입, 서브타이틀, 축 칩, 캐릭터 요약 순서로 구성. SVG는 `<p class="mbti-type">` 위에 삽입
- `streamlit/app.py:83-128` — CSS 블록: `.mbti-card`, `.mbti-type` 등 기존 스타일. 새 `.mbti-animal` 클래스 추가
- 현재 app.py: 789줄, 33KB. streamlit 폴더에 `app.py`와 `environment.yml`만 존재

### Key Measurements

- MBTI_COLORS 패턴: `{"INTJ": "#6C3483", ...}` — 동일 구조로 MBTI_ANIMALS 생성
- 카드 영역: `text-align: center`, 흰색 텍스트, 그라디언트 배경 → SVG도 흰색/반투명 톤으로 카드 위 배치

## Key Technical Decisions

- **SVG를 별도 파일로 분리**: app.py가 이미 789줄/33KB. 16종 SVG(각 ~2-3KB)를 추가하면 ~80KB 증가. `streamlit/animals.py`로 분리해 `MBTI_ANIMALS` 딕셔너리만 import. app.py 파일 크기 부담을 제거하고 SVG 수정 시 카드 로직과 독립적으로 관리 가능
- **SVG 사이즈 80x80px**: 카드 내 `.mbti-type`(56px)과 조화. 너무 크면 카드 레이아웃 깨짐, 너무 작으면 식별 불가. 80px은 인스타 스크린샷에서도 식별 가능한 최소 크기
- **SVG 색상은 흰색/반투명**: 카드 배경이 MBTI_COLORS 그라디언트(진한 색)이므로, SVG는 `fill="white"` 또는 `fill="rgba(255,255,255,0.9)"`로 통일해 가독성 확보

## Open Questions

### Resolved During Planning

- **SVG 배치 위치**: MBTI 타입 글자(`<p class="mbti-type">`) 바로 위에 배치. 이유: 카드 최상단에 시각적 앵커 역할, 서브타이틀/칩/요약과 자연스러운 시각 흐름
- **파일 분리 여부**: `streamlit/animals.py`로 분리. 이유: 33KB app.py에 SVG 코드 추가 시 유지보수 어려움, 500KB 기준 이전에 선제적 분리

### Deferred to Implementation

- 각 동물 SVG의 정확한 path 데이터 — 구현 시 플랫 스타일로 하나씩 제작
- SiS 환경에서 `<svg>` 태그의 inline 렌더링 호환성 — 기본적으로 `st.markdown(unsafe_allow_html=True)`에서 SVG는 지원되지만, 특수 속성(filter, clipPath 등)은 SiS에서 제한될 수 있음

## Implementation Units

- [ ] **Unit 1: MBTI_ANIMALS 딕셔너리 + SVG 16종 제작**

**Goal:** 16종 동물 캐릭터 SVG를 플랫/미니멀 스타일로 제작하고 딕셔너리에 담기

**Requirements:** R1, R2, R3, R4

**Dependencies:** None

**Files:**
- Create: `streamlit/animals.py`

**Approach:**
- `MBTI_ANIMALS` 딕셔너리: key=MBTI 문자열, value=SVG 문자열
- 각 SVG는 `viewBox="0 0 80 80"`, 기본 80x80 크기
- 색상은 `fill="white"` 또는 `fill="rgba(255,255,255,0.85)"` — 카드 배경 위 가독성
- 소품은 단순한 기하학적 형태로 표현 (원, 삼각형, 사각형 조합)
- SVG 내 `filter`, `clipPath`, `use` 등 고급 기능 사용 금지 — SiS 호환성 우선
- 각 동물의 동물 이름을 `MBTI_ANIMAL_NAMES` 딕셔너리로 함께 정의 (카드 아래 "여우", "올빼미" 등 텍스트 표시용)

**Patterns to follow:**
- `streamlit/app.py:30-36` — `MBTI_COLORS` 딕셔너리 구조와 동일한 패턴

**Test expectation:** none — 순수 상수 데이터 파일, 비주얼 검증은 Unit 2 완료 후 앱에서 확인

**Verification:**
- `streamlit/animals.py`에 `MBTI_ANIMALS`(16개 항목)와 `MBTI_ANIMAL_NAMES`(16개 항목) 딕셔너리 존재
- 모든 SVG 문자열이 `<svg` 태그로 시작하고 `</svg>` 태그로 종료
- 16종 각각이 origin 매핑 테이블과 일치 (INTJ=여우, INTP=올빼미, ... ESFP=수달) 및 소품 반영
- `filter`, `clipPath`, `use`, `foreignObject` 등 고급 SVG 기능 미사용

- [ ] **Unit 2: 탭1 MBTI 카드에 캐릭터 통합**

**Goal:** MBTI 카드 HTML에 동물 캐릭터 SVG와 동물 이름을 삽입

**Requirements:** R5, R6

**Dependencies:** Unit 1

**Files:**
- Modify: `streamlit/app.py` (import 추가, CSS 추가, 카드 HTML 수정)

**Approach:**
- `streamlit/animals.py`에서 `MBTI_ANIMALS`, `MBTI_ANIMAL_NAMES` import
- CSS에 `.mbti-animal` 클래스 추가: `text-align: center; margin-bottom: 8px;`
- 카드 HTML에서 `<p class="mbti-type">` 바로 위에 `<div class="mbti-animal">{svg}</div>` 삽입
- 동물 이름은 MBTI 타입 아래, 서브타이틀 위에 작은 텍스트로 표시

**Patterns to follow:**
- `streamlit/app.py:172-185` — 기존 카드 HTML 구조
- `streamlit/app.py:83-128` — 기존 CSS 블록에 새 클래스 추가

**Test expectation:** none — UI 변경, 시각적 검증만 가능 (SiS 배포 후 확인)

**Verification:**
- 앱 실행 시 탭1 MBTI 카드에 동물 캐릭터 SVG가 렌더링됨
- 16종 MBTI 모두에서 해당 동물이 표시됨
- 카드 레이아웃이 깨지지 않음 (SVG가 카드 영역을 넘지 않음)
- 동물 이름 텍스트가 MBTI 타입 아래에 표시됨

## System-Wide Impact

- **Interaction graph:** 탭1 카드 영역만 변경. 탭2(동네 찾기), 탭3(이사 예보)에 영향 없음
- **State lifecycle risks:** 없음 — 순수 프레젠테이션 레이어 변경
- **API surface parity:** 없음 — 프론트엔드 전용 변경
- **Unchanged invariants:** MBTI_COLORS, MBTI_DESC, 데이터 로딩 로직, Cortex AI 호출 모두 변경 없음

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| SiS에서 inline SVG 렌더링 실패 | `filter`/`clipPath` 등 고급 기능 사용 금지. 기본 `path`/`circle`/`rect`만 사용 |
| app.py 파일 크기 증가 | SVG를 `animals.py`로 분리해 app.py 크기 유지 |
| SVG 디자인 일관성 부족 | 모든 SVG를 동일 viewBox(80x80), 동일 fill(white), 동일 스타일(플랫/미니멀)로 통일 |

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-10-mbti-animal-characters-requirements.md](docs/brainstorms/2026-04-10-mbti-animal-characters-requirements.md)
- Related code: `streamlit/app.py` (MBTI_COLORS, 카드 HTML, CSS)
- Related issue: Daterl/dongne-mbti#24
