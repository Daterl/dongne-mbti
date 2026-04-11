# 🏘️ 동네 MBTI

> **AI가 분석한 동네 성격으로 "나에게 맞는 동네"를 찾는 서비스**

[![Snowflake](https://img.shields.io/badge/Snowflake-Cortex%20AI-29B5E8?logo=snowflake)](https://www.snowflake.com)
[![Streamlit](https://img.shields.io/badge/Streamlit%20in%20Snowflake-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://python.org)

**[→ 앱 바로 가기](#)** · **[→ 데모 영상](#)**

---

## 왜 만들었나

이사를 결정할 때 가격, 교통, 학군은 쉽게 찾을 수 있습니다.  
그런데 **"이 동네가 나와 맞는가"** 는 어디서도 알려주지 않습니다.

| 서비스 | 무엇을 알 수 있나 | 빠진 것 |
|--------|-----------------|---------|
| 직방·다방 | 매물 가격, 면적 | 동네 분위기·성격 |
| 호갱노노 | 실거래가 시세 흐름 | 라이프스타일 적합성 |
| 카카오맵 | 주변 시설 위치 | 데이터 기반 동네 정의 |

서울에는 매년 62만 명이 이사를 옵니다 (통계청, 2023).  
평균 탐색 기간은 **4.3개월** — 그 시간 동안 "이 동네가 나랑 맞는지"를 판단할 도구가 없었습니다.

동네 MBTI는 Snowflake Marketplace 데이터(상권·부동산·유동인구·소비)를 교차 분석하여  
서울 3구 55개 동의 성격을 MBTI 16유형으로 정의합니다.

---

## 이런 분들을 위해 만들었어요

**"직방에서 가격은 봤는데, 이 동네 분위기가 나랑 맞는지 모르겠어요"**  
→ Tab 1에서 동네 MBTI를 확인하고, 내 성격과 잘 맞는 동네를 찾아보세요.

**"학군 좋고 조용한 동네를 찾고 싶은데 일일이 검색하기 너무 힘들어요"**  
→ Tab 2에서 "초등학교 근처 조용한 서초구 동네 추천해줘"처럼 자연어로 물어보세요.

**"전세 계약이 만료되는데 지금 이사 타이밍인지 더 기다려야 하는지 모르겠어요"**  
→ Tab 3에서 실거래가 데이터 기반 향후 3개월 시세 전망을 확인하세요.

---

## 핵심 기능

### Tab 1 — 동네 MBTI 카드

서울 3구 55개 동을 4축 데이터로 분석해 MBTI 16유형 중 하나로 분류합니다.

| 축 | 의미 | 데이터 |
|----|------|--------|
| E / I | 활발한 동네 vs 조용한 동네 | 유동인구, 주말 활성도 |
| S / N | 실용적 동네 vs 문화적 동네 | 상권 업종 분포 |
| T / F | 경제 중심 vs 생활 중심 | 자산 수준, 소비 패턴 |
| J / P | 안정적 동네 vs 변화하는 동네 | 시세 변동성, 인구이동 |

동네 카드에서 MBTI 유형 + 성격 요약 + 다른 동네와의 궁합 점수를 확인할 수 있습니다.

> **예시** — 서초구 반포동은 `INTJ`  
> "조용하고 계획적인 분위기. 고자산 1인 가구와 전문직 비율이 높고, 주말보다 평일 활동이 활발한 안정적인 동네."  
> 궁합: 잠원동(INTJ) ★★★★★ · 방배동(ISTJ) ★★★★☆ · 당산동(ENFP) ★★☆☆☆

### Tab 2 — 자연어 동네 찾기

"지하철 2호선 근처에서 조용하고 카페 많은 동네 알려줘"처럼 자연어로 대화하면  
Cortex Search + Cortex Analyst가 조건에 맞는 동네를 추천해줍니다.  
멀티턴 대화를 지원하여 조건을 좁혀가며 탐색할 수 있습니다.

> **대화 예시**
> ```
> 나  : 조용하고 학군 좋은 서초구 동네 추천해줘
> AI  : 반포동(INTJ), 잠원동(INTJ), 서초동(ISTJ)이 적합해요.
>       셋 다 학원가 밀집·낮은 유동인구·안정적 시세가 특징입니다.
> 나  : 전세 2억대로 가능한 곳만 알려줘
> AI  : 조건에 맞는 동네는 방배동입니다. 최근 6개월 전세 중위가 1.9억이에요.
> ```

### Tab 3 — 이사 예보

5년치 실거래가 시계열 데이터를 기반으로 향후 3개월 시세를 예측합니다.  
"지금 이사하면 좋을까?"에 대한 AI 판단을 계절성·인구이동·시세 추이로 제공합니다.

---

## 분석 범위

**서울 3구 55개 동** — 서초구·영등포구·중구

동네 성격을 정밀하게 정의하려면 **동(洞) 단위** 데이터가 필요합니다.  
Snowflake Marketplace에서 SPH + RICHGO가 이 3개 구를 동 단위로 완전히 커버하기 때문에,  
서울 25구 전체를 얕게 다루는 대신 **3구를 깊게 파는 전략**을 선택했습니다.

덕분에 "서초구"가 아닌 "반포동 vs 잠원동"을 구분하는 수준의 분석이 가능합니다.

---

## 데이터

| 소스 | 무엇을 알 수 있나 |
|------|-----------------|
| **SPH** (SKT 유동인구 + KCB 자산/소득 + 신한카드 소비) | 동별 활동성, 소비 업종, 자산 수준 |
| **RICHGO** | 매매·전세 실거래가 이력, 인구이동 추정 |

모두 **Snowflake Marketplace**를 통해 연동 — 외부 크롤링·API 없음.  
데이터 기준: 2021~2026년 | Dynamic Table로 **1일 주기** 자동 갱신.

> **탐색했으나 미채택**: 아정당(Telecom) 데이터는 구(區) 단위만 제공하여  
> 동(洞) 단위 분석에 JOIN이 불가해 최종 파이프라인에서 제외했습니다.

---

## 기술 스택

**Platform**: Snowflake (Streamlit in Snowflake)  
**Language**: Python  
**AI**: Snowflake Cortex AI

| Cortex 기능 | 사용 위치 |
|------------|---------|
| AI_CLASSIFY | 동네 상권 업종 → 라이프스타일 유형 분류 (Tab 1 전처리) |
| AI_COMPLETE | 동네 프로필 텍스트 생성, 이사 전망 해설 (Tab 1·3) |
| CORTEX.SENTIMENT | 동네 프로필 감성 점수 산출 (Dynamic Table 파이프라인) |
| Cortex Search | 동네 프로필 하이브리드(벡터+키워드) 검색 (Tab 2) |
| Cortex Analyst | 자연어 → SQL 변환, Semantic Model 기반 (Tab 2) |
| ML FORECAST | 실거래가 시계열 예측 (Tab 3) |

---

## 아키텍처

```mermaid
graph TB
    A[Snowflake Marketplace\nSPH · RICHGO · Telecom] --> B[DONG_PROFILES\n55개 동 MBTI + 프로필]
    B --> C[Cortex Search\nDONGNE_SEARCH]
    B --> D[Cortex Analyst\nSemantic Model YAML]
    B --> E[Dynamic Table\nDONG_PROFILES_ENRICHED\nTARGET_LAG=1day]
    C --> F[Streamlit in Snowflake]
    D --> F
    E --> F
    B --> F
```

---

## 스크린샷

> *(배포 완료 후 탭별 스크린샷 추가 예정)*

---

## 팀

Snowflake Hackathon 2026 Korea | Tech Track | 2인 팀  
개발 기간: 2026년 4월 1일 ~ 4월 12일
