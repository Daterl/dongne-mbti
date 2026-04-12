# 젠스파크 슬라이드 프롬프트 — 동네 MBTI (최종)

> 사용법: 아래 `---` 사이 전체를 복사 → genspark.ai > AI Slides에 붙여넣기

## 젠스파크에 첨부할 파일 목록

### 1. 템플릿
- `[DOWNLOAD TEMPLATE] Snowflake Hackathon 2026 (External) (3).pptx`

### 2. 앱 스크린샷 (Desktop/ishot/)
| 파일명 | 내용 | 사용 슬라이드 |
|--------|------|-------------|
| `1.jpg` | 탭1 동네 카드 — 내곡동 ESTJ 독수리 + 레이더차트 + 베프/라이벌 | Slide 7 좌측 |
| `2.jpg` | 탭1 궁합 비교 — 내곡동 ESTJ × 반포동 ISTP, 29점 + 캐릭터 대결 | Slide 9 |
| `3.jpg` | 탭2 동네 찾기 — 멀티턴 3턴 대화 (부유한 동네 → ESTP 매칭 → 용산구 범위 안내) | Slide 7 우측 |
| `6.jpg` | 탭4 데이터 탐색 — Cortex Analyst NL2SQL 결과 테이블 2개 | Slide 8 우측 |
| `7.jpg` | 탭3 시세 전망 전체 — 실거래가 추이 + ML 예측 차트 + AI 이사 전망 텍스트 | Slide 8 좌측 |

### 3. MBTI 캐릭터 (Desktop/ㅎㅇ/)
| 파일명 | MBTI | 사용 슬라이드 |
|--------|------|-------------|
| `독수리.png` | ESTJ | Slide 4, 9 (내곡동 예시) |
| `러시안블루.png` | ISTP | Slide 4, 9 (반포동 예시) |
| `햄스터.png` | 대표 캐릭터 | Slide 4 (솔루션 개요) |
| `수달.png` | ESFP | Slide 9 (영등포구 예시) |

> 전체 16종: 거북이, 고양이, 골든리트리버, 도베르만, 독수리, 러시안블루, 말티즈, 사슴, 수달, 아기판다, 앵무새, 여우, 올빼미, 치타, 토끼, 햄스터

---

[페르소나]
당신은 Snowflake 기술 해커톤에서 수상 경험이 있는 데이터 엔지니어링 발표 전문가입니다.
청중은 Snowflake 기술 심사위원 — Cortex AI, Marketplace, 아키텍처에 정통합니다.
발표 스타일:
- "이사 고민"이라는 일상적 공감에서 시작하여 기술 깊이로 자연스럽게 전환
- 추상적 설명 금지 — 반드시 실제 예시("내곡동은 ESTJ 독수리")로 보여주기
- 각 슬라이드에 한 문장 핵심 메시지 + 뒷받침 데이터 구조
- 말투: 전문적이지만 친근하게, 영어 기술 용어는 영어 유지, 나머지는 한국어

첨부한 Snowflake 공식 템플릿 PPTX의 디자인 스타일을 기반으로 새 프레젠테이션을 만들어주세요.
Slide 1(커버)과 마지막 슬라이드(Thank You)는 템플릿 원본 레이아웃을 최대한 유지하세요.
첨부한 앱 스크린샷과 캐릭터 이미지는 아래 슬라이드 스펙에 명시된 위치에 삽입해주세요.

[디자인 시스템]
- 포인트 컬러: #29B5E8 (Snowflake 블루)
- 섹션 헤더: #29B5E8 파란 헤더바 + 흰색 콘텐츠 박스 구조 (템플릿 패턴 그대로)
- 커버/마지막 슬라이드: 다크 배경 / 콘텐츠 슬라이드: 흰색 배경
- 폰트: Bold 섹션 타이틀, 11-13pt 본문
- 총 슬라이드: 13장


[슬라이드별 상세 스펙]


Slide 1 — 커버 (템플릿 표지 그대로)
- 제목: 동네 MBTI
- 서브타이틀: AI로 읽는 동네 성격과 이사 타이밍
- 이름: Diego / Team Daterl
- 날짜: Apr 2026
- 배경: 다크, Snowflake 공식 커버 스타일


Slide 2 — 공감: 이사 고민의 현실
- 제목: "이사할 때 '이 동네가 나와 맞는가?'를 어디서 알 수 있나요?"
- 3개 대형 stat 카드 (가로 배열, 숫자는 60pt+ 대형):
  [카드 1] 43만 명 — 매년 타 지역에서 서울로 이사 오는 인구 (통계청 인구이동통계, 2024)
  [카드 2] 78% — 주거지 선택 시 '동네 분위기·생활환경'을 중요하게 본다 (한국리서치, 2025)
  [카드 3] 0개 — 동네 '성격'을 AI로 정의한 서비스
- 하단 임팩트 문장: "가격·교통은 있다. '이 동네가 나와 맞는가'는 없다."
- 출처: 서울연구원 도시모니터링 data.si.re.kr/smr2024 | 한국리서치 공원이용현황조사 2025
- 레이아웃: 3열 stat 카드 + 하단 강조 박스


Slide 3 — 차별점: 기존 서비스의 한계
- 제목: "기존 서비스는 여기서 멈춘다"
- 비교표 (4행):
  서비스        | 알 수 있는 것          | 빠진 것
  직방·다방    | 매물 가격·면적         | 동네 분위기·성격
  호갱노노     | 실거래가 시세 흐름      | 라이프스타일 적합성
  카카오맵     | 주변 시설 위치          | 데이터 기반 동네 정의
  동네 MBTI    | 위 모두 + AI 동네 성격 + 이사 타이밍 | (없음)
- 마지막 행은 #29B5E8 배경 강조 처리
- 하단: "Snowflake Cortex AI로 '동네 적합성 판단'을 처음 구현"


Slide 4 — 솔루션: 동네 MBTI가 답하는 4가지 질문
- 제목: "동네 MBTI — 4가지 질문에 답한다"
- 4열 카드 (각 파란 상단 헤더 + 흰 본문):
  [탭 1 — 동네 카드] "이 동네 성격은?"
    내곡동 = ESTJ 독수리 "활기찬 생활 밀착형 동네"
    → AI_CLASSIFY + AI_SENTIMENT + AI_COMPLETE
  [탭 2 — 동네 찾기] "나에게 맞는 동네는?"
    "서초구에서 부유한 동네 알려줘" → 잠원동·내곡동·신원동 추천
    → Cortex Agent (Search + Analyst)
  [탭 3 — 시세 전망] "지금 이사해도 될까?"
    최근 평당가 4,222만원 → ML 예측 4,307만원 (+85만원↑)
    → ML FORECAST + AI_COMPLETE
  [탭 4 — 데이터 탐색] "수치로 비교하면?"
    "서초구 외향적인 동네 TOP 3" → SQL 자동 변환 + 결과 테이블
    → Cortex Analyst (Semantic Model YAML)
- 캐릭터 이미지 삽입: 독수리.png(ESTJ), 러시안블루.png(ISTP), 햄스터.png를 탭1 카드 주변에 배치


Slide 5 — 아키텍처 + 기술스택 (템플릿 4분할 레이아웃)
[섹션 1] 문제 정의 — 파란 헤더바
  · 서울 3구(서초·영등포·중) 118개 동을 동(洞) 단위로 분석
  · Marketplace 커버리지가 완전한 구만 선택 → 넓게 얕게가 아닌 좁게 깊게
[섹션 2] 가설 — 파란 헤더바
  · 동네를 MBTI 16유형으로 정의하면 이사 결정의 핵심 질문에 답할 수 있다
  · z-score 정규화 4축 → 16유형 전수 달성 (빈 유형 0개)
[섹션 3] 아키텍처 구조 — 파란 헤더바
  [Marketplace: SPH·RICHGO] → [Snowflake Tables] → [Cortex AI Pipeline]
  → [Dynamic Table TARGET_LAG=1day] → [Streamlit in Snowflake 4탭]
  * 데이터 1바이트도 Snowflake 외부로 나가지 않음
[섹션 4] 사용된 기술 스택 — 파란 헤더바
  · Cortex AI 7종: AI_CLASSIFY, AI_SENTIMENT, AI_COMPLETE, Cortex Search, Cortex Analyst, Cortex Agent, ML FORECAST
  · 데이터: SPH (유동인구·소비·자산), RICHGO (실거래가·인구)
  · 앱: Streamlit in Snowflake, Git integration, Dynamic Table


Slide 6 — Cortex AI 기능 전체 (그리드)
- 제목: "Cortex AI 7개 기능 — 모두 실제로 동작한다"
- 그리드 (각 카드: 파란 상단 + 흰 설명):
  AI_CLASSIFY    | 동네 상권 → 라이프스타일 유형 6카테고리 자동 분류
  AI_SENTIMENT   | 동네 프로필 감성 점수 → 탭1 카드 색상화
  AI_COMPLETE    | 동네 성격 요약 텍스트 + 이사 전망 해설 생성
  Cortex Search  | "조용한 동네" 자연어 하이브리드 검색 (탭2)
  Cortex Analyst | 자연어→SQL 자동 변환, Semantic Model YAML 기반 (탭4)
  Cortex Agent   | Search + Analyst 오케스트레이션, 멀티턴 대화 (탭2)
  ML FORECAST    | 118개 시계열 시세 예측, 이사 타이밍 판단 (탭3)
- 하단 강조: "AI 결과는 테이블 저장 → 매 클릭 무호출 · 비용 $40 이내 완결"


Slide 7 — 앱 데모: 동네 카드 & 동네 찾기
- 제목: "실제 앱 — 동네 카드 & 자연어 검색"
- 2열 레이아웃:
  [좌] 첨부 이미지 1.jpg 삽입
    캡션: "내곡동 ESTJ 독수리 — 레이더차트·궁합 점수·베프/라이벌 캐릭터"
  [우] 첨부 이미지 3.jpg 삽입
    캡션: "서초구에서 부유한 동네 → ESTP 매칭 → 멀티턴 3턴 대화"
- 하단 태그: AI_CLASSIFY · AI_SENTIMENT · AI_COMPLETE · Cortex Agent


Slide 8 — 앱 데모: 시세 전망 & 데이터 탐색
- 제목: "실제 앱 — 이사 예보 & NL2SQL 분석"
- 2열 레이아웃:
  [좌] 첨부 이미지 7.jpg 삽입
    캡션: "서초구 내곡동 — 실거래가 추이 + ML 3개월 예측 + AI 이사 전망"
  [우] 첨부 이미지 6.jpg 삽입
    캡션: "서초구 외향적 동네 TOP 3 → Cortex Analyst SQL 자동 변환"
- 하단 태그: ML FORECAST · Cortex Analyst · AI_COMPLETE


Slide 9 — Insight #1: 동네 MBTI가 발견한 것
- 제목: "Insight & Recommendations #1: 118개 동 분석이 드러낸 서울의 성격"
[핵심 분석 인사이트] — 파란 헤더바, 흰 박스
  · 내곡동 = ESTJ 독수리: "활기찬 생활 밀착형, 실용적 소비, 안정적 시세"
  · 영등포3가 = ESFP 수달: "젊은 층 활발, 카페·엔터 소비, 변동성 높음"
  · 궁합 점수: 내곡동(ESTJ) × 반포동(ISTP) = 29점 "다른 세계관, 충돌 주의"
  · 16 MBTI 유형 전수 달성 — 데이터가 자연스럽게 동네 성격을 만들어냄
[향후 실행 방안 제안] — 파란 헤더바, 흰 박스
  · 사용자 본인 MBTI 입력 → 궁합 동네 자동 매칭 추천
  · 서울 25구 전체 확장 (Marketplace 데이터 확대 시)
[기대 효과] — 파란 헤더바, 흰 박스
  · "내곡동은 ESTJ 독수리" 한 문장으로 전달되는 동네 성격 이해
  · 이사 고민 탐색 시간 단축: 데이터 기반 즉시 판단
- 캐릭터 이미지 삽입: 독수리.png(ESTJ 내곡동) + 수달.png(ESFP 영등포3가) 배치


Slide 10 — Insight #2: 이사 타이밍 예측 결과
- 제목: "Insight & Recommendations #2: ML FORECAST가 본 이사 타이밍"
[핵심 분석 인사이트] — 파란 헤더바, 흰 박스
  · RICHGO 2022~2024 실거래 시계열 124개월 → 118개 시리즈 ML FORECAST
  · 서초구 내곡동: 최근 평당가 4,222만원 → 3개월 후 예측 4,307만원 (+85만원↑)
  · 2023년 저점(~3,800만원) 이후 완만한 회복세 — 상승 초입 진입
[향후 실행 방안 제안] — 파란 헤더바, 흰 박스
  · 계절성·인구이동·시세 변동을 결합한 "이사 적기 지수" 지표화
  · 사용자 전세 만료 시점 입력 → 맞춤 이사 타이밍 알림
[기대 효과] — 파란 헤더바, 흰 박스
  · "지금 이사하면 좋을까?" 질문에 데이터 기반 근거 제시
  · 감으로 하던 이사 타이밍 결정을 AI 예측으로 대체


Slide 11 — Insight #3: 확장 전략
- 제목: "Insight & Recommendations #3: 3구에서 전국으로"
[핵심 분석 인사이트] — 파란 헤더바, 흰 박스
  · 3구 딥다이브 전략 검증: Marketplace 커버리지 기반 데이터 완결성 100%
  · 자연어 검색 멀티턴 대화로 실제 사용 흐름 검증 완료
  · 비용 $40 이내 완결: 배치 패턴 + XSMALL Warehouse + 증분 인덱싱
[향후 실행 방안 제안] — 파란 헤더바, 흰 박스
  · Phase 2: 서울 25구 전체 (Marketplace 데이터 확대 시)
  · Phase 3: 개인 MBTI ↔ 동네 MBTI 매칭 개인화 추천
  · Phase 4: 전국 주요 도시 + 부동산 플랫폼 파트너십
[기대 효과] — 파란 헤더바, 흰 박스
  · TAM: 연 43만 명(서울 전입) → 전국 수백만 명
  · Snowflake Data Cloud 기반 B2B SaaS 전환
  · 부동산 플랫폼 White-label 공급


Slide 12 — 왜 Snowflake인가
- 제목: "왜 Snowflake여야 하는가"
- 2열 레이아웃:
  [좌] Cortex AI 체크리스트 (각 파란 체크마크):
    ✓ AI_CLASSIFY — SQL 파이프라인 직접 내장
    ✓ AI_SENTIMENT — Dynamic Table 자동 갱신
    ✓ AI_COMPLETE — 배치 저장, 매 클릭 무호출
    ✓ Cortex Search — 하이브리드 검색, 1일 증분 인덱싱
    ✓ Cortex Analyst — Semantic Model YAML 기반 NL2SQL
    ✓ Cortex Agent — Search + Analyst 오케스트레이션
    ✓ ML FORECAST — 118 시리즈 시계열 예측
  [우] 강조 박스 3개 (대형 텍스트):
    "외부 서버 0개"
    "외부 API 0개"
    "100% Snowflake 내부 완결"
  하단: GitHub: github.com/Daterl/dongne-mbti


Slide 13 — Thank You (템플릿 마지막 슬라이드 그대로)
- "THANK YOU"
- 하단: GitHub: github.com/Daterl/dongne-mbti
- Snowflake Hackathon 2026 Korea | Tech Track | Team Daterl


[추가 지시사항]
- 섹션 헤더는 반드시 #29B5E8 파란 바 + 흰 콘텐츠 박스 구조 (템플릿 패턴)
- Slide 5는 반드시 4분할 레이아웃 (템플릿 원본 구조와 동일)
- Slide 9·10·11은 반드시 3섹션 구조 — 핵심인사이트/향후실행방안/기대효과 (템플릿 Insight 구조)
- Slide 7·8은 스크린샷 중심 — 텍스트는 캡션만 최소한으로
- 스피커 노트: 각 슬라이드 30초 분량 추가
- 실제 예시 데이터("내곡동 = ESTJ 독수리" 등)는 반드시 포함 — 추상적 설명 금지
- 첨부 이미지 파일명을 정확히 매칭해서 해당 슬라이드에 삽입

---
