# 데이터 소스 및 MBTI 4축 매핑 가이드

## Marketplace 데이터

총 3개 데이터 소스, Snowflake Marketplace를 통해 연동. 외부 크롤링·API 없음.

---

### 1. RICHGO — 실거래가 + 인구

DB: `KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA`  
스키마: `HACKATHON_2025Q2` | 테이블 3개

#### REGION_APT_RICHGO_MARKET_PRICE_M_H
아파트 시세 데이터 (매매/전세 평당가)
| 컬럼 | 타입 | 설명 |
|------|------|------|
| BJD_CODE | TEXT | 법정동 코드 |
| SD / SGG / EMD | TEXT | 시도 / 시군구 / 읍면동 |
| MEME_PRICE_PER_SUPPLY_PYEONG | FLOAT | 매매 평당가 |
| JEONSE_PRICE_PER_SUPPLY_PYEONG | FLOAT | 전세 평당가 |
| TOTAL_HOUSEHOLDS | NUMBER | 총 세대수 |
| YYYYMMDD | DATE | 기준일 |

#### REGION_MOIS_POPULATION_GENDER_AGE_M_H
성별/연령별 인구 데이터
| 컬럼 | 타입 | 설명 |
|------|------|------|
| TOTAL / MALE / FEMALE | NUMBER | 전체/남/여 인구 |
| AGE_UNDER20 ~ AGE_OVER70 | NUMBER | 연령대별 인구수 (7개 구간) |
| BJD_CODE, SD, SGG, EMD | TEXT | 지역 코드 |

#### REGION_MOIS_POPULATION_AGE_UNDER5_PER_FEMALE_20TO40_M_H
영유아 비율 데이터

**활용**: 탭 1 (T/F축 매매가, J/P축 변동성), 탭 3 (시세 시계열 + ML FORECAST)

---

### 2. SPH — 유동인구 + 소비 + 자산

DB: `SEOUL_DISTRICTLEVEL_DATA_FLOATING_POPULATION_CONSUMPTION_AND_ASSETS`  
스키마: `GRANDATA` | 테이블 5개

#### FLOATING_POPULATION_INFO
SKT 유동인구 데이터
| 컬럼 | 타입 | 설명 |
|------|------|------|
| RESIDENTIAL_POPULATION | FLOAT | 거주 인구 |
| WORKING_POPULATION | FLOAT | 근무 인구 |
| VISITING_POPULATION | FLOAT | 방문 인구 |
| AGE_GROUP / GENDER | TEXT | 연령대 / 성별 |
| WEEKDAY_WEEKEND | TEXT | 평일/주말 |

#### CARD_SALES_INFO
신한카드 소비 데이터 (업종별 매출)
| 주요 업종 컬럼 | 설명 |
|----------------|------|
| FOOD_SALES | 식품 |
| COFFEE_SALES | 커피 |
| ENTERTAINMENT_SALES | 오락 |
| SPORTS_CULTURE_LEISURE_SALES | 스포츠/문화/레저 |
| MEDICAL_SALES | 의료 |
| EDUCATION_ACADEMY_SALES | 교육/학원 |
| E_COMMERCE_SALES | 이커머스 |
| TOTAL_SALES | 전체 합계 |

#### ASSET_INCOME_INFO
KCB 자산/소득 데이터
| 주요 컬럼 | 설명 |
|----------|------|
| AVERAGE_INCOME / MEDIAN_INCOME | 평균/중위 소득 |
| AVERAGE_ASSET_AMOUNT | 평균 자산 |
| AVERAGE_SCORE | 평균 신용점수 |
| OWN_HOUSING_COUNT | 주택 보유 수 |

#### M_SCCO_MST
지역 마스터 (시/구/동 한영 명칭 + 지리 정보)

**활용**: 탭 1 (E/I축 유동인구, S/N축 소비패턴, T/F축 자산/소득), 탭 2 (자연어 검색)

---

### 3. DataKnows — AI 추정 시세 + 역세권

2026년 최신 매매·전세 AI 추정 시세 + 지하철역 접근성 데이터.

**활용**: 탭 1 (T/F축 매매가 보조), 탭 3 (최신 시세 반영)

---

### 탐색했으나 미채택

| 데이터 | 미채택 사유 |
|--------|-----------|
| 아정당 (Telecom) | 구(區) 단위만 제공 → 동(洞) 단위 분석에 JOIN 불가 |
| 넥스트레이드 (NextTrade) | 주식 시장 데이터 → 동네 성격 분석과 직접 관련 없음 |

---

## DB 간 JOIN 전략

### 지역 코드 매핑

| DB | 지역 키 | 단위 |
|----|---------|------|
| RICHGO | `BJD_CODE` + `SD`/`SGG`/`EMD` | 법정동 |
| SPH | `PROVINCE_CODE`/`CITY_CODE`/`DISTRICT_CODE` | 행정구 |

### JOIN 경로

```
RICHGO ←(SD/SGG/EMD)→ DONGNE_MASTER ←(PROVINCE/CITY/DISTRICT_CODE)→ SPH
```

> **주의**: RICHGO는 읍면동(EMD) 단위, SPH는 구(DISTRICT) 단위. 구 단위로 통일하거나 RICHGO를 SGG 기준 집계.

---

## MBTI 4축 ↔ 데이터 매핑

> **스코프**: 서초구·영등포구·중구 118개 동

### E/I (활동성) — SPH 유동인구

| 피처 | 산식 | E 방향 |
|------|------|--------|
| 방문비율 | `VISITING / (RESIDENTIAL + WORKING + VISITING)` | 높을수록 E |
| 주말비율 | 주말 유동인구 / 전체 유동인구 | 높을수록 E |
| 유흥비율 | `ENTERTAINMENT_SALES / TOTAL_SALES` | 높을수록 E |

### S/N (라이프스타일) — SPH 카드소비

| 피처 | 산식 | 방향 |
|------|------|------|
| 실용소비율 | `(FOOD + MEDICAL) / TOTAL` | 높을수록 S |
| 문화소비율 | `(COFFEE + ENTERTAINMENT + SPORTS_CULTURE) / TOTAL` | 높을수록 N |

### T/F (경제력) — SPH 자산 + RICHGO 시세 + DataKnows

| 피처 | 산식 | T 방향 |
|------|------|--------|
| 평균소득 | `AVG(AVERAGE_INCOME)` | 높을수록 T |
| 평균자산 | `AVG(AVERAGE_ASSET_AMOUNT)` | 높을수록 T |
| 매매평당가 | `AVG(MEME_PRICE_PER_SUPPLY_PYEONG)` | 높을수록 T |

### J/P (안정성) — RICHGO 변동성

| 피처 | 산식 | 방향 |
|------|------|------|
| 시세변동성 | `STDDEV(MEME_PRICE) / AVG(MEME_PRICE)` | 높을수록 P |
| 청년비율 | `(AGE_20S + AGE_30S) / TOTAL` | 높을수록 P |

> **판정**: 각 축별 z-score 정규화 후 평균. 양수면 앞글자(E/S/T/J), 음수면 뒷글자(I/N/F/P).  
> **SQL**: `sql/schema/02_dong_features.sql`, `03_dong_mbti_result.sql`

---

## Cortex AI 활용 매핑

| 기능 | 역할 | 탭 | 상태 |
|------|------|-----|------|
| AI_CLASSIFY | 동네 유형 6카테고리 분류 | 탭 1 | ✅ 동작 |
| AI_SENTIMENT | 동네 프로필 감성 분석 (92% 정확도) | 탭 1 | ✅ 동작 |
| AI_COMPLETE | 프로필 텍스트 생성 + 이사 전망 | 탭 1, 3 | ✅ 동작 |
| Cortex Search | 하이브리드 검색 (벡터+키워드, 12%↑) | 탭 2 | ✅ 동작 |
| Cortex Analyst | NL2SQL (90%+, Semantic Model YAML) | 탭 4 | ✅ 동작 |
| Cortex Agent | Search + Analyst 오케스트레이션 | — | 📋 DDL만 (Trial 제약) |
| ML FORECAST | 118개 시계열 시세 예측 | 탭 3 | ✅ 동작 |
