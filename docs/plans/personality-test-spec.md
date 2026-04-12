# 성향 테스트 탭 설계 스펙

> 리서치 4종(디자인 시스템, UX 레퍼런스, AI 프롬프트, SiS 제약) 종합

## 1. 플로우 아키텍처

**통합 방식: Full-page gate (탭 추가 X)**

퀴즈가 랜딩 페이지. 완료/건너뛰기 후 기존 4탭 등장. `st.stop()`으로 퀴즈 중 탭 렌더링 차단.

```
앱 로드
  │
  ├─ quiz_completed == False ─→ 전체화면 퀴즈 + st.stop()
  │     0 = 인트로 (CTA: "시작하기" + "바로 둘러보기 >")
  │     1-8 = 질문 (한 화면에 한 문제씩)
  │     9 = 분석 중 (2초 펄스 애니메이션)
  │     10 = 결과 (DNA + TOP 3 + "동네 둘러보기" CTA)
  │
  └─ quiz_completed == True ─→ 결과 배너 + 기존 4탭 (코드 변경 0)
```

## 2. UI 구성 요소

### 2.1 인트로 (step=0)
- 타이틀: "🧭 나의 동네 DNA 테스트"
- 서브: "8개의 질문으로 118개 동네 중 당신에게 딱 맞는 곳을 찾아드려요"
- 동물 캐릭터 3-4개 미리보기 (base64 이미지)
- CTA 버튼: "시작하기" → quiz_step = 1

### 2.2 질문 (step=1~8)
- **프로그레스 바**: CSS 그라디언트 바 + "질문 N / 8" 텍스트
- **질문 카드**: emoji + title + question
- **선택지**: st.button × 4 (use_container_width=True, on_click 콜백)
- **버튼 스타일**: border-radius: 16px, hover 시 파란 테두리 + 살짝 올라감
- **전환 애니메이션**: fadeSlideIn (opacity 0→1, translateY 12px→0, 0.35s)

### 2.3 분석 중 (step=9)
- 펄스 애니메이션 이모지 (🔍)
- "당신의 동네 DNA를 분석하고 있어요..."
- time.sleep(2) → quiz_step = 10 → st.rerun()

### 2.4 결과 (step=10)

**Phase A: 나의 동네 DNA**
- MBTI 유형 + 동물 캐릭터 (기존 MBTI_ANIMALS 재사용)
- 4축 칩 (기존 axis-chip 클래스 재사용)
- AI DNA 분석 텍스트 (AI_COMPLETE, 3-4문장)
- 인사이트 갭 (선택적: Q1 답변 vs 최종 결과 차이)

**Phase B: TOP 3 매칭**
- 3위 → 2위 → 1위 순서로 카드 표시
- 각 카드: MBTI 카드 미니 버전 + 매칭률 + AI 추천 이유 (2-3문장)
- 축별 비교 바 (사용자 vs 동네 시각적 비교)

**Phase C: 이사 결정 카드**
- 1위 동네의 시세 전망 (ML Forecast 데이터 연동)
- AI 이사 타이밍 판단 (AI_COMPLETE, 2-3문장)
- 결과 요약 카드 (스크린샷용, max-width: 400px)

## 3. 기술 명세

### 3.1 통합 위치
- **탭 추가 아님.** 퀴즈는 탭 앞의 full-page gate.
- 기존 `st.tabs()` 호출(line 458) 앞에 조건 분기 삽입
- `st.stop()`으로 퀴즈 중 탭 렌더링 완전 차단
- 기존 4탭 코드 변경 = 0줄

### 3.2 Session State
```python
quiz_step: int          # 0~10
quiz_answers: list[int] # 0~3 인덱스 × 8개
quiz_completed: bool
quiz_user_scores: dict  # {"EI": float, ...}
quiz_user_mbti: str     # "ENFP"
quiz_matches: list      # TOP 3 결과
quiz_dna_text: str      # AI 생성 텍스트
```

### 3.3 AI 호출 (총 5-6회, ~$0.0012/세션)
| 호출 | 모델 | temp | max_tokens | 용도 |
|------|------|------|------------|------|
| DNA 분석 | llama3.3-70b | 0.7 | 300 | 성향 요약 3-4문장 |
| 인사이트 갭 | llama3.3-70b | 0.7 | 200 | 의식/무의식 차이 (선택적) |
| 추천 이유 ×3 | llama3.3-70b | 0.7 | 250 | 동네별 추천 근거 |
| 이사 전망 | llama3.3-70b | 0.4 | 250 | 시세 기반 판단 |

### 3.4 폴백 체인
```
llama3.3-70b (ARRAY_CONSTRUCT) 
  → snowflake-arctic (단일 문자열)
  → 정적 텍스트 (Python 포맷팅)
```

### 3.5 CSS 규칙 (기존 디자인 시스템 준수)
- border-radius: 24px (카드), 16px (버튼/서브카드), 14px (정보박스)
- 그라디언트: 135deg 대각선, rgba 저투명도
- 그림자: 카드 = `0 12px 40px rgba(0,0,0,0.25)`
- 폰트: 제목 22px/700, 본문 14-15px, 라벨 13px/600
- 전환: all 0.2s ease (hover), width 0.6s ease (바)

### 3.6 SiS 주의사항
- st.experimental_rerun() → **st.rerun()** 사용
- CSS @keyframes 지원됨
- time.sleep(2) 사용 가능 (분석 중 화면)
- AI_COMPLETE 1-3회/페이지 안전, 5회도 OK
- base64 이미지 인라인 가능

## 4. Cortex AI 파이프라인 (6개 기능 연쇄)

| 단계 | Cortex 기능 | 용도 |
|------|------------|------|
| 기 | (없음) | 순수 Python 스코어링 |
| 승 | AI_COMPLETE | DNA 분석 텍스트 생성 |
| 승 | AI_CLASSIFY | (기존 저장값: NEIGHBORHOOD_TYPE) |
| 전 | Cortex Search | 프로필 텍스트 기반 동네 매칭 보조 |
| 전 | AI_COMPLETE | 추천 이유 생성 (×3) |
| 전 | AI_SENTIMENT | (기존 저장값: SENTIMENT_SCORE) |
| 결 | Cortex Analyst | 시세 데이터 조회 |
| 결 | AI_COMPLETE | 이사 타이밍 판단 |

## 5. 파일 변경 사항

| 파일 | 변경 |
|------|------|
| streamlit/app.py | 탭 추가 + 퀴즈 플로우 코드 (~300줄) + `st.experimental_rerun()` → `st.rerun()` 교체 (6곳, 완료) |
| streamlit/questions.py | ×3 스케일링 팩터 적용 + `reset_quiz_state()` 추가 + match_pct 조정 (완료) |
| streamlit/animals.py | 수정 불필요 (기존 재사용) |

## 5.1 리뷰 반영 사항 (Important 6개)

| # | 항목 | 해결 방법 | 상태 |
|---|------|----------|------|
| 1 | 점수 스케일 불일치 | `SCORE_SCALE_FACTOR = 3.0` 적용, match_pct 계수 조정 | 완료 |
| 2 | 뒤로 가기 / 다시 하기 | `reset_quiz_state()` 함수 추가, 결과 화면에 "다시 하기" 버튼 | 코드 반영 완료, UI 구현 시 적용 |
| 3 | Cortex Search 역할 | TOP 3 추천 이유 생성 시 PROFILE_TEXT를 Cortex Search로 조회하여 context 보강 | 구현 시 적용 |
| 4 | 결과 로딩 시간 | Phase A(DNA) 먼저 표시 → spinner → Phase B(TOP 3) 점진적 렌더링 | 구현 시 적용 |
| 5 | 성공 기준(DoD) | 인트로 → 8문제 → 분석 → MBTI 카드 + DNA + TOP 3 + 시세 → 전체 렌더링 | 명시 |
| 6 | 기존 rerun 교체 | app.py 6곳 `st.experimental_rerun()` → `st.rerun()` | 완료 |

## 6. 심사 기준 대응

| 심사 항목 (배점) | 이 기능이 기여하는 점 |
|-----------------|-------------------|
| 창의성 25% | "나를 입력하면 동네가 나온다" — 기존 서비스 대비 완전한 차별화 |
| Snowflake 전문성 25% | 6개 Cortex 기능 하나의 파이프라인으로 엮음 |
| AI 전문성 25% | "단순 기능이 아닌 가치 창출 구조" 직접 해당 |
| 현실성 15% | 기존 앱에 자연스럽게 통합, 완성도 높음 |
| 스토리텔링 10% | 기승전결 데모 시나리오 완성 |
