# 젠스파크 슬라이드 프롬프트 — 동네 MBTI (v2 최종)

> 사용법: 아래 `---` 사이 전체를 복사 → genspark.ai > AI Slides에 붙여넣기

## 젠스파크에 첨부할 파일 목록 (총 14개)

### 1. 템플릿
- `[DOWNLOAD TEMPLATE] Snowflake Hackathon 2026 (External) (3).pptx`

### 2. 앱 스크린샷 (assets/screenshots/)
| 파일명 | 내용 | 사용 슬라이드 |
|--------|------|-------------|
| `landing-quiz.png` | 랜딩 퀴즈 — "집을 구할 때, 당신의 첫 번째 조건은?" | Slide 4 |
| `landing-result.png` | 랜딩 결과 — "당신에게 딱 맞는 동네 TOP 3" (ENFP 매칭) | Slide 4 |
| `tab1-dong-card.jpg` | 탭1 — 내곡동 ESTJ 독수리 카드 + 레이더차트 | Slide 8 |
| `tab1-compatibility.jpg` | 탭1 — 궁합 비교 29점 (ESTJ × ISTP 캐릭터 대결) | Slide 8 |
| `tab2-dong-search.jpg` | 탭2 — 멀티턴 3턴 대화 | Slide 9 |
| `tab3-price-forecast.jpg` | 탭3 — 실거래가 추이 + ML 예측 + AI 이사 전망 | Slide 9 |
| `tab4-data-explorer.jpg` | 탭4 — Cortex Analyst NL2SQL 결과 테이블 | Slide 10 |

### 3. 아키텍처
| 파일명 | 사용 슬라이드 |
|--------|-------------|
| `architecture.jpg` | Slide 6 |

### 4. MBTI 캐릭터 (Desktop/ㅎㅇ/)
| 파일명 | MBTI | 사용 슬라이드 |
|--------|------|-------------|
| `독수리.png` | ESTJ | Slide 5, 11 |
| `러시안블루.png` | ISTP | Slide 5 |
| `햄스터.png` | 대표 | Slide 5 |
| `수달.png` | ESFP | Slide 11 |

### 5. 팀 프로필
| 파일명 | 사용 슬라이드 |
|--------|-------------|
| `profile-jangwon.png` (윤장원) | Slide 1, 14 |

---

[페르소나]
당신은 Snowflake 기술 해커톤에서 수상 경험이 있는 데이터 엔지니어링 발표 전문가입니다.
청중은 Snowflake 기술 심사위원 — Cortex AI, Marketplace, 아키텍처에 정통합니다.
발표 스타일:
- "이사 고민"이라는 일상적 공감에서 시작하여 기술 깊이로 자연스럽게 전환
- 추상적 설명 금지 — 반드시 실제 예시("내곡동은 ESTJ 독수리")와 스크린샷으로 보여주기
- 각 슬라이드에 한 문장 핵심 메시지 + 뒷받침 데이터
- 모든 통계에는 출처 표기 (각주 또는 하단 작은 텍스트)
- 말투: 전문적이지만 친근하게, 영어 기술 용어는 영어 유지, 나머지는 한국어

첨부한 Snowflake 공식 템플릿 PPTX의 디자인 스타일을 기반으로 새 프레젠테이션을 만들어주세요.
Slide 1(커버)과 마지막 슬라이드(Thank You)는 템플릿 원본 레이아웃을 최대한 유지하세요.
첨부한 앱 스크린샷, 아키텍처 이미지, 캐릭터 이미지는 아래 슬라이드 스펙에 명시된 위치에 삽입해주세요.

[디자인 시스템]
- 포인트 컬러: #29B5E8 (Snowflake 블루)
- 섹션 헤더: #29B5E8 파란 헤더바 + 흰색 콘텐츠 박스 구조 (템플릿 패턴)
- 커버/마지막 슬라이드: 다크 배경 / 콘텐츠 슬라이드: 흰색 배경
- 폰트: Bold 섹션 타이틀, 11-13pt 본문
- 총 슬라이드: 14장
- 통계 출처: 각 슬라이드 하단 8pt 회색 텍스트로 표기


[슬라이드별 상세 스펙]


Slide 1 — 커버 (템플릿 표지 스타일)
- 제목: 동네 MBTI
- 서브타이틀: AI로 읽는 동네 성격과 이사 타이밍
- 팀: Team Daterl
  · 윤장원 (Diego) — github.com/jangwonyoon
  · 조원제 — github.com/onejaejae
- 날짜: Apr 2026
- 배경: 다크, Snowflake 공식 커버 스타일
- 첨부된 프로필 이미지(profile-jangwon.png) 삽입 가능하면 우측 하단에 작게 배치


Slide 2 — 공감: 이사 고민의 현실
- 제목: "이사할 때 '이 동네가 나와 맞는가?'를 어디서 알 수 있나요?"
- 3개 대형 stat 카드 (가로 배열, 숫자는 60pt+ 대형):
  [카드 1] 43만 명 — 매년 타 지역에서 서울로 이사 오는 인구
  [카드 2] 78% — 주거지 선택 시 '동네 환경'을 중요하게 본다
  [카드 3] 41% — 부동산 앱 정보와 실제의 일치율
- 하단 임팩트 문장: "가격·교통은 있다. '이 동네가 나와 맞는가'는 없다."
- 출처 (하단 8pt): 통계청 인구이동통계 2024 | 한국리서치 2024.11 | 한국소비자원 2018


Slide 3 — 차별점: 기존 서비스의 한계
- 제목: "645만 MAU가 쓰는 부동산 앱, 동네 성격은 0개"
- 비교표 (5행):
  서비스        | MAU        | 제공 정보              | 빠진 것
  직방          | 229만      | 매물 가격·면적         | 동네 성격
  호갱노노      | 179만      | 실거래가 시세           | 라이프스타일 적합성
  네이버 부동산  | 134만      | 매물·시세·뉴스         | 데이터 기반 동네 정의
  다방          | 103만      | 매물·실거래가          | 동네 분위기
  동네 MBTI     | —          | 위 모두 + AI 동네 성격 + 이사 타이밍 | (없음)
- 마지막 행 #29B5E8 강조
- 하단: "한국 PropTech 시장 2.3조 원, 5년 8배 성장 — 그런데 '동네 적합성'은 아직 공백"
- 출처 (하단 8pt): 와이즈앱 2024.01 | 한국프롭테크포럼 2023


Slide 4 — 솔루션: 동네 MBTI 사용 흐름
- 제목: "8가지 질문 → 나에게 맞는 동네 TOP 3"
- 2열 레이아웃:
  [좌] 첨부 이미지 landing-quiz.png 삽입
    캡션: "이사 조건, 주말 라이프, 산책 취향 등 8가지 질문"
  [우] 첨부 이미지 landing-result.png 삽입
    캡션: "당신의 동네 MBTI는 ENFP! 딱 맞는 동네 TOP 3"
- 하단: "답변 → MBTI 4축 매핑 → Cortex AI 매칭 → 개인화 동네 추천"
- 캐릭터 이미지 삽입: 독수리.png, 러시안블루.png, 햄스터.png를 결과 화면 주변에 배치


Slide 5 — 핵심 기능 4탭 요약
- 제목: "동네 MBTI — 4가지 질문에 답한다"
- 4열 카드 (각 파란 상단 헤더 + 흰 본문):
  [탭 1 — 동네 카드] "이 동네 성격은?"
    내곡동 = ESTJ 독수리 "활기찬 생활 밀착형"
    AI_CLASSIFY + AI_SENTIMENT + AI_COMPLETE
  [탭 2 — 동네 찾기] "나에게 맞는 동네는?"
    "부유한 서초구 동네 알려줘" → 멀티턴 대화
    Cortex Search + AI_COMPLETE
  [탭 3 — 시세 전망] "지금 이사해도 될까?"
    평당가 4,222만원 → 예측 4,307만원 (+85만원)
    ML FORECAST + AI_COMPLETE
  [탭 4 — 데이터 탐색] "수치로 비교하면?"
    "서초구 E점수 TOP 3" → SQL 자동 변환
    Cortex Analyst (NL2SQL 90%+ 정확도)


Slide 6 — 아키텍처 (이미지)
- 제목: "Snowflake 풀스택 아키텍처"
- 첨부 이미지 architecture.jpg 삽입 (전체 슬라이드 크기로)
- 하단 캡션: "Marketplace → Cortex AI Pipeline → Dynamic Table → Streamlit in Snowflake"


Slide 7 — Cortex AI 기능 (그리드 + 벤치마크)
- 제목: "Cortex AI 6개 기능 실동작 + ML FORECAST"
- 그리드 (각 카드: 파란 상단 + 흰 설명):
  AI_CLASSIFY    | 동네 상권 → 6개 라이프스타일 유형 자동 분류 ✅
  AI_SENTIMENT   | 감성 분석 92% 정확도 (GPT-4.1 83% 대비) ✅
  AI_COMPLETE    | 동네 프로필 + 이사 전망 생성 (Fallback 자동 전환) ✅
  Cortex Search  | 하이브리드 검색, 단순 벡터 대비 12%↑ (NDCG@10) ✅
  Cortex Analyst | NL2SQL 90%+, GPT-4o 대비 2배 정확 ✅
  ML FORECAST    | 118개 시계열 시세 예측, ON_ERROR: SKIP ✅
  Cortex Agent   | DDL 설계 완료 (Trial 계정 제약) 📋
- 하단 강조: "AI 결과는 테이블 저장 → 매 클릭 무호출 · $40 예산 완결"
- 출처 (하단 8pt): Snowflake Engineering Blog 2024-2025


Slide 8 — 앱 데모: 동네 카드 (탭 1)
- 제목: "실제 앱 — 동네 카드 & 궁합 비교"
- 2열 레이아웃:
  [좌] 첨부 이미지 tab1-dong-card.jpg 삽입
    캡션: "내곡동 ESTJ 독수리 — 레이더차트 4축 점수 + 베프/라이벌"
  [우] 첨부 이미지 tab1-compatibility.jpg 삽입
    캡션: "내곡동(ESTJ) × 반포동(ISTP) = 궁합 29점 '다른 세계관'"
- 하단 태그: AI_CLASSIFY · AI_SENTIMENT · AI_COMPLETE


Slide 9 — 앱 데모: 동네 찾기 & 시세 전망 (탭 2, 3)
- 제목: "실제 앱 — 자연어 검색 & 이사 예보"
- 2열 레이아웃:
  [좌] 첨부 이미지 tab2-dong-search.jpg 삽입
    캡션: "서초구 부유한 동네 → ESTP 매칭 → 용산구 범위 안내 (3턴)"
  [우] 첨부 이미지 tab3-price-forecast.jpg 삽입
    캡션: "내곡동 124개월 실거래 + ML 3개월 예측 4,307만원"
- 하단 태그: Cortex Search · ML FORECAST · AI_COMPLETE


Slide 10 — 앱 데모: 데이터 탐색 (탭 4)
- 제목: "실제 앱 — NL2SQL 데이터 분석"
- 전체 이미지: 첨부 이미지 tab4-data-explorer.jpg 삽입
- 캡션: "서초구 외향적 동네 TOP 3 / 서초구 부유한 동네 TOP 3 → SQL 자동 변환"
- 하단: "Cortex Analyst — Semantic Model YAML (5 Tables, 7 Verified Queries)"
- 출처 (하단 8pt): NL2SQL 90%+ 정확도, Snowflake Engineering Blog


Slide 11 — Insight #1: 동네 MBTI가 발견한 것
- 제목: "Insight & Recommendations #1: 118개 동이 드러낸 서울의 성격"
[핵심 분석 인사이트] — 파란 헤더바, 흰 박스
  · 내곡동 = ESTJ 독수리: "활기찬 생활 밀착, 실용적 소비, 안정적 시세"
  · 영등포3가 = ESFP 수달: "젊은 층, 카페·엔터 소비, 변동성 높음"
  · 16 MBTI 유형 전수 달성 — 데이터가 자연스럽게 동네 성격을 만들어냄
  · 학술 근거: Rentfrow et al.(2013) 150만 명 미국 3개 성격 지역 분류 선례
  · 한국 MBTI: 18-35세 93% 검사 경험, Google Trends 세계 1위 (2위의 6배)
[향후 실행 방안 제안] — 파란 헤더바, 흰 박스
  · 사용자 MBTI 입력 → 궁합 동네 매칭 (Jokela 2015 Person-Environment Fit 기반)
  · 서울 25구 확장 (Marketplace 데이터 확대 시)
[기대 효과] — 파란 헤더바, 흰 박스
  · "내곡동은 ESTJ 독수리" 한 문장으로 동네 성격 전달
  · 이사 탐색 → 데이터 기반 즉시 판단
- 캐릭터: 독수리.png + 수달.png 배치
- 출처 (하단 8pt): Rentfrow et al. 2013, J.Personality | 한국리서치


Slide 12 — Insight #2: 이사 타이밍 & 비용 합리성
- 제목: "Insight & Recommendations #2: ML이 본 이사 타이밍 & $40 완결"
[핵심 분석 인사이트] — 파란 헤더바, 흰 박스
  · 124개월 실거래 시계열 → 118개 시리즈 ML FORECAST
  · 서초구 내곡동: 4,222만원 → 3개월 후 4,307만원 (+85만원↑)
  · 비용 $40 완결: 배치 패턴 + XSMALL + AUTO_SUSPEND=60 + 증분 인덱싱
[향후 실행 방안 제안] — 파란 헤더바, 흰 박스
  · "이사 적기 지수" 지표화 (계절성 + 시세 + 인구이동 결합)
  · 전세 만료 시점 입력 → 맞춤 이사 타이밍 알림
[기대 효과] — 파란 헤더바, 흰 박스
  · "지금 이사하면 좋을까?" → 데이터 기반 답변
  · 이사 서비스 시장 3~3.5조 원 중 온라인 침투율 1% 미만 → 기회


Slide 13 — Insight #3: 확장 전략
- 제목: "Insight & Recommendations #3: 3구에서 전국으로"
[핵심 분석 인사이트] — 파란 헤더바, 흰 박스
  · 3구 딥다이브 전략 검증: 데이터 완결성 100%, 16유형 전수 달성
  · 자연어 멀티턴 대화 + NL2SQL 실사용 흐름 검증 완료
  · 부동산 앱 이용자 44%가 2030세대 → 동네 MBTI 타겟 직결
[향후 실행 방안 제안] — 파란 헤더바, 흰 박스
  · Phase 2: 서울 25구 전체 (Marketplace 확대 시)
  · Phase 3: 개인 MBTI ↔ 동네 MBTI 매칭 개인화
  · Phase 4: 전국 + 부동산 플랫폼 파트너십
[기대 효과] — 파란 헤더바, 흰 박스
  · TAM: 연 43만(전입) + 79만(서울 내) = 122만 건 → 전국 수백만
  · PropTech 2.3조 원 시장, 앱 MAU 645만+ 중 동네 적합성 공백 선점
  · Snowflake Data Cloud 기반 B2B SaaS 전환
- 출처 (하단 8pt): 한국프롭테크포럼 2023 | 와이즈앱 2024


Slide 14 — Thank You + 팀 소개 (템플릿 마지막 슬라이드 스타일)
- "THANK YOU" (다크 배경)
- 팀 소개 (2열):
  [좌] 윤장원 (Diego)
    GitHub: github.com/jangwonyoon
    프로필 이미지: profile-jangwon.png 삽입
  [우] 조원제
    GitHub: github.com/onejaejae
- 하단:
  · 프로젝트: github.com/Daterl/dongne-mbti
  · Snowflake Hackathon 2026 Korea | Tech Track | Team Daterl
- 100% Snowflake Internal: 외부 서버 0개 · 외부 API 0개


[추가 지시사항]
- 섹션 헤더는 반드시 #29B5E8 파란 바 + 흰 콘텐츠 박스 구조 (템플릿 패턴)
- Slide 6은 아키텍처 이미지를 슬라이드 전체에 배치 (최대 크기)
- Slide 11·12·13은 반드시 3섹션 구조 — 핵심인사이트/향후실행방안/기대효과
- Slide 8·9·10은 스크린샷 중심 — 텍스트는 캡션만
- 스피커 노트: 각 슬라이드 30초 분량 추가
- 실제 예시 데이터는 반드시 포함 — 추상적 설명 금지
- 모든 통계에 출처 표기 (슬라이드 하단 8pt 회색)
- 첨부 이미지 파일명을 정확히 매칭해서 해당 슬라이드에 삽입

---
