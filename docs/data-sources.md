# 데이터 소스 및 Cortex AI / CoCo 스킬 활용 가이드

## Marketplace 데이터 (설치 완료)

총 4개 데이터베이스, 26개 테이블, 553개 컬럼.

---

### 1. 리치고 (Dataknows) — `KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA`

스키마: `HACKATHON_2025Q2` | 테이블 3개

#### REGION_APT_RICHGO_MARKET_PRICE_M_H
아파트 시세 데이터 (매매/전세 평당가)
| 컬럼 | 타입 | 설명 |
|------|------|------|
| BJD_CODE | TEXT | 법정동 코드 |
| SD / SGG / EMD | TEXT | 시도 / 시군구 / 읍면동 |
| REGION_LEVEL | TEXT | 지역 단위 |
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
| YYYYMMDD | DATE | 기준일 |

#### REGION_MOIS_POPULATION_AGE_UNDER5_PER_FEMALE_20TO40_M_H
영유아 비율 데이터
| 컬럼 | 타입 | 설명 |
|------|------|------|
| AGE_UNDER5 | NUMBER | 5세 미만 인구 |
| FEMALE_20TO40 | NUMBER | 20~40세 여성 인구 |
| AGE_UNDER5_PER_FEMALE_20TO40 | FLOAT | 가임여성 대비 영유아 비율 |

**활용**: 탭 1(MBTI 4축), 탭 3(이사 예보 시세 시계열)

---

### 2. SPH — `SEOUL_DISTRICTLEVEL_DATA_FLOATING_POPULATION_CONSUMPTION_AND_ASSETS`

스키마: `GRANDATA` | 테이블 5개

#### FLOATING_POPULATION_INFO
SKT 유동인구 데이터
| 컬럼 | 타입 | 설명 |
|------|------|------|
| RESIDENTIAL_POPULATION | FLOAT | 거주 인구 |
| WORKING_POPULATION | FLOAT | 근무 인구 |
| VISITING_POPULATION | FLOAT | 방문 인구 |
| AGE_GROUP / GENDER | TEXT | 연령대 / 성별 |
| TIME_SLOT | TEXT | 시간대 |
| WEEKDAY_WEEKEND | TEXT | 평일/주말 |
| CITY_CODE / DISTRICT_CODE / PROVINCE_CODE | TEXT | 지역 코드 |
| STANDARD_YEAR_MONTH | TEXT | 기준 년월 |

#### CARD_SALES_INFO
신한카드 소비 데이터 (업종별 매출)
| 주요 업종 컬럼 | 설명 |
|----------------|------|
| FOOD_SALES / FOOD_COUNT | 식품 |
| COFFEE_SALES / COFFEE_COUNT | 커피 |
| ENTERTAINMENT_SALES | 오락 |
| SPORTS_CULTURE_LEISURE_SALES | 스포츠/문화/레저 |
| MEDICAL_SALES | 의료 |
| EDUCATION_ACADEMY_SALES | 교육/학원 |
| BEAUTY_SALES | 미용 |
| E_COMMERCE_SALES | 이커머스 |
| TOTAL_SALES / TOTAL_COUNT | 전체 합계 |

분류: AGE_GROUP, GENDER, LIFESTYLE, TIME_SLOT, WEEKDAY_WEEKEND, CARD_TYPE

#### ASSET_INCOME_INFO
KCB 자산/소득 데이터 (110+ 컬럼)
| 주요 컬럼 그룹 | 설명 |
|----------------|------|
| AVERAGE_INCOME / MEDIAN_INCOME | 평균/중위 소득 |
| AVERAGE_HOUSEHOLD_INCOME | 가구 평균 소득 |
| AVERAGE_ASSET_AMOUNT | 평균 자산 |
| AVERAGE_SCORE | 평균 신용점수 |
| RATE_INCOME_*M | 소득 구간별 비율 |
| RATE_MODEL_GROUP_* | 직업군별 비율 |
| AVERAGE_*_BALANCE_AMOUNT | 대출잔액 (은행/비은행/주택/신용) |
| OWN_HOUSING_COUNT / MULTIPLE_HOUSING_COUNT | 주택 보유 |
| PYEONG_*_COUNT | 평수별 주거 |

#### CODE_MASTER
코드 마스터 테이블 (지역 코드 매핑)

#### M_SCCO_MST
지역 마스터 (시/구/동 한영 명칭 + 지리 정보)
| 컬럼 | 설명 |
|------|------|
| DISTRICT_KOR_NAME / DISTRICT_ENG_NAME | 구 이름 |
| DISTRICT_GEOM (GEOGRAPHY) | 지리 공간 데이터 |

**활용**: 탭 1(MBTI E/I축=유동인구, S/N축=소비패턴, T/F축=자산/소득), 탭 2(자연어 검색)

---

### 3. 넥스트레이드 (NextTrade) — `NEXTRADE_EQUITY_MARKET_DATA`

스키마: `FIN` | 테이블 7개

| 테이블 | 설명 |
|--------|------|
| NX_HT_BAT_REFER_A0 | 종목 기본 정보 (종목코드, 상장일, 시가총액 등) |
| NX_HT_ONL_MKTPR_A3 | 실시간 시세 (시가/고가/저가/종가/거래량) |
| NX_HT_ONL_MKTPR_B6 | 호가 10단계 (매수/매도 호가 및 잔량) |
| NX_HT_ONL_MKTPR_E1 | 매수/매도 총잔량 |
| NX_HT_ONL_STATS_B5 | 시장 등락 통계 (상한가/하한가 종목 수) |
| NX_HT_ONL_STATS_C3 | 차익/비차익 거래 통계 |
| NX_HT_ONL_STATS_P0 | 투자자 유형별 매매 동향 |

**활용**: 탭 3(부가 경제지표 — 주식시장 흐름과 부동산 상관관계 분석)

---

### 4. 아정당 (AJD) — `SOUTH_KOREA_TELECOM_SUBSCRIPTION_ANALYTICS__...`

스키마: `TELECOM_INSIGHTS` | 테이블 11개

| 테이블 | 설명 |
|--------|------|
| V01_MONTHLY_REGIONAL_CONTRACT_STATS | 월별 지역별 계약 통계 |
| V02_SERVICE_BUNDLE_PATTERNS | 서비스 번들 패턴 (인터넷+TV+전화) |
| V03_CONTRACT_FUNNEL_CONVERSION | 계약 전환율 퍼널 |
| V04_CHANNEL_CONTRACT_PERFORMANCE | 채널별 계약 성과 |
| V05_REGIONAL_NEW_INSTALL | 지역별 신규 설치 |
| V06_RENTAL_CATEGORY_TRENDS | 렌탈 카테고리 트렌드 |
| V07_GA4_MARKETING_ATTRIBUTION | GA4 마케팅 기여도 |
| V08_GA4_DEVICE_STATS | GA4 디바이스 통계 |
| V09_MONTHLY_CALL_STATS | 월별 상담 통계 |
| V10_HOURLY_CALL_DISTRIBUTION | 시간대별 상담 분포 |
| V11_CALL_TO_CONTRACT_CONVERSION | 상담→계약 전환율 |

**활용**: 탭 1(J/P축=안정vs변화 — 신규설치/해지 패턴으로 이사 추정), 탭 3(이사 시기 예측)

---

## Cortex AI 활용 매핑

| 기능 | 역할 | 적용 탭 |
|------|------|---------|
| AI_CLASSIFY | 데이터 → MBTI 4축 분류 | 탭 1 |
| AI_SENTIMENT | 동네 리뷰/뉴스 감성 분석 | 탭 1 |
| AI_COMPLETE | MBTI 성격 요약 + 이사 전망 생성 | 탭 1, 3 |
| Cortex Search | 동네 프로필 하이브리드 검색 (벡터+키워드) | 탭 2 |
| Cortex Analyst | 자연어→SQL (Semantic Model 기반) | 탭 2, 3 |
| Cortex Agent | Search+Analyst 자동 라우팅 | 탭 2 |

---

## CoCo (Cortex Code) 스킬 활용 가이드

Snowflake Cortex Code(CoCo)는 Snowsight 내장 AI 코딩 어시스턴트로, 10개의 스킬을 제공합니다.
동네 MBTI 프로젝트에서 활용 가능한 스킬을 우선순위별로 정리합니다.

### 핵심 활용 (필수)

| # | 스킬 | 설명 | 프로젝트 활용 |
|---|------|------|---------------|
| 1 | **cortex-ai-functions** | AI 분석, 감성, 요약, 번역, OCR | MBTI 분류(AI_CLASSIFY), 감성분석(AI_SENTIMENT), 텍스트 생성(AI_COMPLETE) — 프로젝트 핵심 |
| 9 | **machine-learning** | ML 학습, 레지스트리, 추론 | MBTI 4축 클러스터링 모델 학습, 이사 시기 예측 모델 구축 |
| 10 | **notebooks-in-workspaces** | 노트북 생성/편집/실행 | EDA, 데이터 전처리, MBTI 축 로직 프로토타이핑 |

### 적극 활용 (권장)

| # | 스킬 | 설명 | 프로젝트 활용 |
|---|------|------|---------------|
| 5 | **data-quality** | DMF, 품질 모니터링, 검증 | Marketplace 데이터 품질 검증 (NULL 비율, 이상치 탐지) |
| 7 | **integrations** | API, 스토리지, 외부 연결 | Streamlit 앱에서 Cortex API 연동, 외부 데이터 보조 연결 |
| 8 | **lineage** | 의존성, 영향분석, 출처 추적 | 4개 DB 간 데이터 계보 파악, 변환 파이프라인 추적 |

### 보조 활용 (선택)

| # | 스킬 | 설명 | 프로젝트 활용 |
|---|------|------|---------------|
| 2 | **cost-intelligence** | 비용, 크레딧, 예산, 최적화 | 트라이얼 크레딧 소진 모니터링 (30일 제한!) |
| 4 | **data-governance** | 마스킹, 분류, 권한, 컴플라이언스 | Marketplace 데이터 접근 권한 설정 |

### 비해당 (이 프로젝트에서는 불필요)

| # | 스킬 | 사유 |
|---|------|------|
| 3 | **data-cleanrooms** | 외부 조직과 데이터 협업 없음 |
| 6 | **dbt-projects-on-snowflake** | dbt 미사용 (직접 SQL + Streamlit) |

### CoCo 활용 예시 (Snowsight에서 Cmd+I)

```
-- cortex-ai-functions 활용
"유동인구와 소비 데이터로 동네별 E/I 성향을 분류하는 AI_CLASSIFY 쿼리를 작성해줘"

-- machine-learning 활용
"리치고 시세 데이터로 향후 3개월 아파트 가격을 예측하는 ML 모델을 만들어줘"

-- notebooks-in-workspaces 활용  
"CARD_SALES_INFO 테이블의 업종별 소비 패턴을 EDA하는 노트북을 만들어줘"

-- data-quality 활용
"4개 마켓플레이스 DB의 NULL 비율과 데이터 최신성을 점검해줘"

-- cost-intelligence 활용
"현재 크레딧 사용량과 남은 트라이얼 기간을 확인해줘"
```

---

## MBTI 4축 ↔ 데이터 매핑

| MBTI 축 | 의미 | 핵심 데이터 | 테이블 |
|---------|------|-------------|--------|
| **E/I** (활동성) | 외향적 vs 내향적 동네 | 유동인구(방문/거주/근무 비율), 시간대별 활동량 | FLOATING_POPULATION_INFO |
| **S/N** (실용vs문화) | 실용적 vs 문화적 동네 | 업종별 소비 비율 (식품/의료 vs 카페/문화/레저) | CARD_SALES_INFO |
| **T/F** (경제vs생활) | 경제중심 vs 생활중심 동네 | 소득/자산/신용점수 vs 주거평수/가구 구성 | ASSET_INCOME_INFO |
| **J/P** (안정vs변화) | 안정적 vs 변화하는 동네 | 인구 변동률, 신규설치/해지 패턴, 시세 변동성 | 인구데이터 + V01/V05 + 시세 |

---

## Snowflake 계정 정보

- **계정**: `ehlanwg/ps28769`
- **사용자**: `jangwonyoon` (ACCOUNTADMIN)
- **리전**: AWS
- **계정 유형**: 트라이얼 (30일)
