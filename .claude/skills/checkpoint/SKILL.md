---
name: checkpoint
description: "개발 페이즈 완료 시 종합 체크포인트를 GitHub Wiki에 기록하는 스킬. 페이즈가 끝났을 때, 마일스톤 달성 시, '체크포인트', '페이즈 완료', '단계 정리', 'phase 리뷰', '중간 점검', '진행 점검', '마일스톤', '단계 끝', '페이즈 정리' 등의 요청 시 반드시 이 스킬을 사용한다. /checkpoint로 트리거한다."
version: "1.1"
category: workflow
---

# Checkpoint — 페이즈 완료 체크포인트 → GitHub Wiki

개발 페이즈 완료 시 산출물, 분석 결과, 의사결정, 리스크를 종합하여 Wiki 체크포인트 페이지를 생성한다.

페이즈 정의, 페이지 템플릿, Decision 템플릿: `references/checkpoint-template.md` 참조.

## 워크플로우

### Step 1: 페이즈 식별

사용자 요청 또는 현재 날짜/진행 상황에서 완료된 페이즈를 식별한다.
- 사용자가 "Phase 1 체크포인트" 명시 → 해당 페이즈
- 명시 없으면 → 날짜 기반 추정 (4/8→Phase 1, 4/9→Phase 2, ...)

### Step 2: 정보 수집

**자동 수집:**

1. **git log**: 해당 페이즈 기간의 전체 커밋
   ```bash
   git log --since="{시작일} 00:00" --until="{종료일} 23:59" --oneline --stat
   ```

2. **GitHub Issues**: 해당 기간 닫힌 이슈
   ```bash
   gh issue list --state closed --search "closed:{시작일}..{종료일}" --json number,title,labels
   ```

3. **파일 변경**: 해당 기간 생성/수정된 파일 목록
   ```bash
   git diff --name-status HEAD~$(git log --since="{시작일}" --oneline | wc -l)..HEAD
   ```

4. **Daily Logs**: 이전에 작성된 Daily Log 위키 페이지를 읽어 정보 종합

**사용자 보충 질문:**
- 크레딧 사용량 (누적)
- 주요 기술 의사결정
- 발견된 리스크 변화
- 다음 Phase 계획 조정 사항

### Step 3: 체크포인트 페이지 생성

wiki-writer 에이전트를 서브 에이전트로 호출. 템플릿: `references/checkpoint-template.md`를 Read한 뒤 적용.

```
Agent(
  subagent_type: "wiki-writer",
  model: "opus",
  prompt: "Checkpoint 페이지를 작성하라. 템플릿은 references/checkpoint-template.md를 Read하여 따르라. Phase: {N}, 수집 정보: {Step 2 결과}"
)
```

**출력 파일**: `Checkpoint-Phase-{N}.md`

### Step 4: Home 페이지 + 사이드바 업데이트

1. Home.md의 진행 현황 테이블에서 해당 Phase를 "완료"로 업데이트
2. _Sidebar.md에 체크포인트 페이지 링크 추가

### Step 5: Wiki 푸시

```bash
cd /tmp/dongne-mbti-wiki
git add "Checkpoint-Phase-{N}.md" "Home.md" "_Sidebar.md"
git commit -m "docs: Phase {N} checkpoint"
git push
```

### Step 6 (선택): Decision 페이지

페이즈 중 중요한 기술 의사결정이 있었다면 별도 Decision 페이지도 생성한다.

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| 페이즈 식별 불가 | 사용자에게 "어떤 Phase의 체크포인트인가요?" 질문 |
| Daily Log가 없음 | git log + issues만으로 체크포인트 작성 |
| 목표 대비 달성이 부족 | "부분 완료" 상태로 정직하게 기록, 이월 작업을 다음 Phase 계획에 추가 |
| wiki 리포 접근 불가 | 로컬 파일 생성 후 수동 푸시 안내 |

## 테스트 시나리오

### 정상 흐름
**프롬프트**: "/checkpoint" 또는 "Phase 1 체크포인트 기록해줘"
**기대 결과**:
1. Phase 1 (4/8, 데이터 준비) 식별
2. git log에서 5건 커밋, 3건 이슈 수집
3. Daily-Log-2026-04-08.md 참조
4. 사용자에게 크레딧/의사결정 질문
5. Checkpoint-Phase-1.md 생성 (목표 vs 실제 테이블 포함)
6. Home.md 진행 현황 업데이트
7. wiki 리포에 커밋+푸시

### 에러 흐름
**프롬프트**: Phase 2 시작 전에 "/checkpoint"
**기대 결과**:
1. Phase 1의 목표 중 일부 미달성 감지
2. "부분 완료" 상태로 기록
3. 미완료 항목을 Phase 2 계획에 이월 제안
