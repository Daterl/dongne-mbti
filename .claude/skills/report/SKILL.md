---
name: report
description: "일일 개발 리포트를 GitHub Wiki에 기록하는 스킬. 티켓이 완료되었을 때, 하루 개발이 끝났을 때, '리포트', '일일 로그', '오늘 작업 정리', '위키에 기록', 'daily log', '개발 일지', '진행 상황 기록' 등의 요청 시 반드시 이 스킬을 사용한다. /report로 트리거한다."
---

# Report — 일일 개발 리포트 → GitHub Wiki

완료된 티켓과 당일 작업을 GitHub Wiki Daily Log 페이지에 기록한다.

## 워크플로우

### Step 1: 정보 수집

다음 소스에서 자동으로 정보를 수집한다:

1. **git log**: 오늘 날짜의 커밋 목록
   ```bash
   git log --since="today 00:00" --oneline --no-merges
   ```

2. **git diff --stat**: 변경된 파일 목록과 규모
   ```bash
   git diff --stat HEAD~$(git log --since="today 00:00" --oneline | wc -l)..HEAD
   ```

3. **GitHub Issues**: 오늘 닫힌 이슈
   ```bash
   gh issue list --state closed --search "closed:>=$(date +%Y-%m-%d)" --json number,title
   ```

4. **사용자 보충**: 수집 결과를 보여주고, 추가 내용 (크레딧 사용량, 발견 사항, 내일 계획)을 질문

### Step 2: Wiki 페이지 생성

wiki-writer 에이전트를 서브 에이전트로 호출하여 Daily Log 페이지를 생성한다.
템플릿: `references/daily-log-template.md`를 Read한 뒤 적용.

```
Agent(
  subagent_type: "wiki-writer",
  model: "opus",
  prompt: "Daily Log 페이지를 작성하라. 템플릿은 references/daily-log-template.md를 Read하여 따르라. 날짜: {오늘}, 수집된 정보: {Step 1 결과}"
)
```

**출력 파일**: `Daily-Log-{YYYY-MM-DD}.md`

### Step 3: Wiki 푸시

```bash
cd /tmp/dongne-mbti-wiki
git add "Daily-Log-{YYYY-MM-DD}.md" "_Sidebar.md"
git commit -m "docs: Daily Log {YYYY-MM-DD}"
git push
```

Wiki 리포가 클론되어 있지 않으면:
```bash
git clone https://github.com/Daterl/dongne-mbti.wiki.git /tmp/dongne-mbti-wiki
```

### Step 4: Home 페이지 업데이트

Home.md의 진행 현황 섹션을 오늘 기준으로 업데이트한다.

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| git log가 비어있음 | 사용자에게 수동 입력 요청 |
| gh CLI 미설치/인증 실패 | 커밋 메시지에서 이슈 번호를 파싱 |
| wiki 리포 접근 불가 | 로컬 파일로 생성 후 수동 푸시 안내 |
| 크레딧 정보 없음 | "미확인" 표기, 사용자에게 Snowflake에서 확인 요청 |

## 테스트 시나리오

### 정상 흐름
**프롬프트**: "/report" 또는 "오늘 작업 위키에 기록해줘"
**기대 결과**:
1. git log에서 오늘 커밋 3건 수집
2. gh issue에서 닫힌 이슈 2건 수집
3. 사용자에게 크레딧/내일 계획 질문
4. Daily-Log-2026-04-08.md 생성
5. _Sidebar.md 업데이트
6. wiki 리포에 커밋+푸시

### 에러 흐름
**프롬프트**: 커밋이 0건인 날 "/report"
**기대 결과**:
1. git log 비어있음 감지
2. 사용자에게 "오늘 커밋이 없습니다. 수동으로 작업 내용을 입력해주세요" 안내
3. 사용자 입력 기반으로 Daily Log 생성
