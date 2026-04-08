# EDA 결과 — Issue #4

> 실행일: 2026-04-08 | Phase 1: 데이터 준비

## 1. 테이블 오버뷰

### 행 수
| 테이블 | 행 수 | 단위 |
|--------|-------|------|
| 리치고_시세 | 4,356 | 동×월 (서울 emd 단위) |
| SPH_유동인구 | 2,577,120 | 동×월×성별×연령×시간대×요일 |
| SPH_카드소비 | 6,208,957 | 동×월×카드×요일×성별×연령×시간대×라이프스타일 |
| SPH_자산소득 | 269,159 | 동×월 |
| SPH_지역마스터 | 467 | 서울 전체 동 목록 |

### 지역 커버리지
- SPH 지역마스터: 467개 동 (서울 전체)
- 리치고: emd(읍면동) 단위, SD='서울'
- SPH: DISTRICT_CODE(동) 단위, PROVINCE_KOR_NAME='서울특별시'

### 시간 범위
| 테이블 | 확인된 기간 |
|--------|-----------|
| 리치고_시세 | 2019-06 ~ 2023-12 |
| 리치고_인구 | 2025-01 (최신) |

### 컬럼 확인 완료
- **카드소비 20개 업종**: FOOD, COFFEE, ENTERTAINMENT, DEPARTMENT_STORE, LARGE_DISCOUNT_STORE, SMALL_RETAIL_STORE, CLOTHING_ACCESSORIES, SPORTS_CULTURE_LEISURE, ACCOMMODATION, TRAVEL, BEAUTY, HOME_LIFE_SERVICE, EDUCATION_ACADEMY, MEDICAL, ELECTRONICS_FURNITURE, CAR, CAR_SERVICE_SUPPLIES, GAS_STATION, E_COMMERCE (각 _SALES + _COUNT)
- **인구 연령**: AGE_UNDER20, AGE_20S, AGE_30S, AGE_40S, AGE_50S, AGE_60S, AGE_OVER70
- **시세**: MEME_PRICE_PER_SUPPLY_PYEONG, JEONSE_PRICE_PER_SUPPLY_PYEONG

---

## 2. MBTI 4축 피처 분포

### E/I 축 (활동성): 외향적 vs 내향적 동네
| 피처 | 범위 | 변별력 | 채택 |
|------|------|--------|------|
| 방문인구 비율 (visit_ratio) | 0.22 ~ 3.97 | 18배 차이, 우수 | **O** |
| 주말 유동인구 비중 (weekend_ratio) | 미실행 | — | O (후보) |
| 엔터테인먼트 소비 비중 (ent_ratio) | 미실행 | — | O (후보) |

- visit_ratio 상위 (E): DISTRICT_CODE 11140106(3.97), 11140108(3.67), 11140104(2.95)
- visit_ratio 하위 (I): 11650103(0.22), 11560118(0.27), 11560133(0.30)
- CITY_CODE 3개 확인: 11140(중구 추정), 11560(영등포구 추정), 11650(서초구 추정)

### S/N 축 (실용 vs 문화): 실용적 vs 문화적 동네
| 피처 | 데이터 소스 | 채택 |
|------|-----------|------|
| 실용(FOOD+MEDICAL+GAS_STATION) vs 문화(COFFEE+SPORTS_CULTURE_LEISURE+TRAVEL) | CARD_SALES_INFO | **O** |
| 대형마트(LARGE_DISCOUNT_STORE) vs 이커머스(E_COMMERCE) 비율 | CARD_SALES_INFO | **O** |
| 교육/학원(EDUCATION_ACADEMY) 비중 | CARD_SALES_INFO | O (보조) |

### T/F 축 (경제 vs 생활): 경제중심 vs 생활중심 동네
| 피처 | 데이터 소스 | 채택 |
|------|-----------|------|
| 평균 소득 (AVERAGE_INCOME) | ASSET_INCOME_INFO (NULL 0%) | **O** |
| 고소득 비율 (RATE_INCOME_OVER_70M) | ASSET_INCOME_INFO (NULL 0%) | **O** |
| 신용 점수 (AVERAGE_SCORE) | ASSET_INCOME_INFO (NULL 0%) | O (보조) |
| 주택 보유율 (OWN_HOUSING_COUNT/CUSTOMER_COUNT) | ASSET_INCOME_INFO | **O** |
| 전세가율 (JEONSE/MEME) | RICHGO_MARKET_PRICE | **O** |
| 영유아 비율 (AGE_UNDER5_PER_FEMALE_20TO40) | RICHGO_POPULATION | O (F 보조) |

### J/P 축 (안정 vs 변화): 안정적 vs 변화하는 동네
| 피처 | 데이터 소스 | 채택 |
|------|-----------|------|
| 시세 변동계수 (STDDEV/AVG) | RICHGO_MARKET_PRICE | **O** |
| 20~30대 비율 (AGE_20S+AGE_30S/TOTAL) | RICHGO_POPULATION | **O** |
| 인구 변화율 (최신 vs 과거) | RICHGO_POPULATION | O (후보) |

---

## 3. 데이터 품질

### NULL 비율
| 테이블 | 핵심 컬럼 | NULL% | 판정 |
|--------|----------|-------|------|
| SPH_자산소득 | AVERAGE_INCOME, MEDIAN_INCOME, AVERAGE_ASSET_AMOUNT, AVERAGE_SCORE, OWN_HOUSING_COUNT, RATE_INCOME_OVER_70M | **0.00%** | OK |

### 주요 이슈
1. **인구 0인 동 존재**: 양화동 등 일부 동의 인구가 0 (폐동/비거주) → MBTI 계산 시 제외 필요
2. **카드소비 0값**: 세분화된 데이터(성별×연령×시간대)라 개별 셀에 0이 많음 → 구별 집계 시 해소
3. **리치고 행 수 4,356**: 서울 467동 대비 적음 → 일부 동만 아파트 시세 존재. 누락 동 파악 필요

---

## 4. JOIN 키 검증

### 리치고 ↔ SPH 매핑
- 리치고: `SD='서울'`, `SGG='영등포구'`, `EMD='여의도동'`
- SPH: `PROVINCE_KOR_NAME='서울특별시'`, `CITY_KOR_NAME='종로구'`, `DISTRICT_KOR_NAME='청운동'`
- **매핑 전략**: 리치고.SGG = SPH.CITY_KOR_NAME (구 이름 텍스트 매칭)
- **주의**: 리치고 SD='서울' ≠ SPH PROVINCE_KOR_NAME='서울특별시'

### 데이터 단위
- 리치고: emd (읍면동) 단위
- SPH: DISTRICT_CODE (동) 단위
- **구 단위 통일 필요**: 리치고를 SGG 기준 집계, SPH를 CITY_CODE 기준 집계

---

## 5. 결론: 4축별 확정 피처

| 축 | 확정 피처 | 데이터 소스 | 정규화 |
|----|----------|------------|--------|
| E/I | visit_ratio, weekend_ratio, ent_ratio | FLOATING_POPULATION_INFO, CARD_SALES_INFO | z-score |
| S/N | practical_to_cultural, mart_to_ecom, edu_ratio | CARD_SALES_INFO | z-score |
| T/F | avg_income, high_income_rate, own_housing_rate, jeonse_ratio, child_ratio | ASSET_INCOME_INFO, RICHGO_MARKET_PRICE, RICHGO_POPULATION | z-score |
| J/P | price_cv, young_ratio, pop_change_rate | RICHGO_MARKET_PRICE, RICHGO_POPULATION | z-score |

### MBTI 판정 로직
각 축별 피처를 z-score 정규화 → 가중평균 → 양수면 첫 글자(E/S/T/J), 음수면 둘째 글자(I/N/F/P)

### 다음 단계 (#5 스키마 설계 반영 사항)
- DONGNE_MASTER 테이블: SPH M_SCCO_MST 기반, 리치고 SGG 매핑 컬럼 포함
- 구 단위(SGG/CITY_CODE) 집계 뷰 필요 — MVP는 구 단위(25개)
- 리치고-SPH 지역명 매핑 테이블 또는 JOIN 조건 정의
- 인구 0인 동 제외 로직
