# MBTI 4축 매핑 로직 — Issue #6

> 스코프: 서초구·영등포구·중구 118개 동  
> SQL: `sql/schema/02_dong_features.sql`, `sql/schema/03_dong_mbti_result.sql`  
> 실행 결과: 118동, 16종 MBTI 전수 분류 완료

## 데이터 흐름

```
SPH(유동인구/카드소비/자산) ─┐
RICHGO(시세/인구)          ──┤── DONG_FEAT_EI/SN/TF/JP ── DONG_MBTI_RESULT
                             │        (원본 피처)               (z-score + MBTI)
DONGNE_MASTER(JOIN 허브)  ──┘
```

## 4축 피처 설계

### E/I (활동성) — DONG_FEAT_EI

| 피처 | 산식 | 방향 | 소스 |
|------|------|------|------|
| visit_ratio | VISITING / RESIDENTIAL | E↑ | SPH FLOATING_POPULATION |
| weekend_ratio | 주말(H) 유동인구 / 전체 | E↑ | SPH FLOATING_POPULATION |
| ent_ratio | (ENTERTAINMENT + SPORTS_CULTURE_LEISURE) / TOTAL_SALES | E↑ | SPH CARD_SALES |

> ⚠️ WEEKDAY_WEEKEND 실제값: `'H'` (휴일/주말). `'WEEKEND'`/`'주말'` 아님.

### S/N (라이프스타일) — DONG_FEAT_SN

| 피처 | 산식 | 방향 | 소스 |
|------|------|------|------|
| practical_ratio | (FOOD + MEDICAL) / TOTAL_SALES | S↑ | SPH CARD_SALES |
| edu_ratio | EDUCATION_ACADEMY / TOTAL_SALES | S↑ | SPH CARD_SALES |
| culture_ratio | (COFFEE + ENTERTAINMENT + SPORTS_CULTURE_LEISURE) / TOTAL | **N↑** | SPH CARD_SALES |

> ⚠️ culture_ratio는 N 방향 → 03에서 z-score 부호 반전 적용.

### T/F (경제수준) — DONG_FEAT_TF

| 피처 | 산식 | 방향 | 소스 |
|------|------|------|------|
| avg_income | AVG(AVERAGE_INCOME) | T↑ | SPH ASSET_INCOME |
| avg_asset | AVG(AVERAGE_ASSET_AMOUNT) | T↑ | SPH ASSET_INCOME |
| avg_price | AVG(MEME_PRICE_PER_SUPPLY_PYEONG) COALESCE(동→구) | T↑ | RICHGO 시세 |

### J/P (안정성) — DONG_FEAT_JP

| 피처 | 산식 | 방향 | 소스 |
|------|------|------|------|
| price_cv | STDDEV(MEME_PRICE) / AVG(MEME_PRICE) COALESCE(동→구) | P↑ | RICHGO 시세 |
| young_ratio | (AGE_20S + AGE_30S) / TOTAL COALESCE(동→구) | P↑ | RICHGO 인구 |

## z-score 정규화 → MBTI 판정

```sql
-- 공통 패턴 (03_dong_mbti_result.sql)
AVG(z_score) OVER (전체 118동) = 0, STDDEV = 1

-- 축별 점수 산식
ei_score = (z_visit + z_weekend + z_ent) / 3
sn_score = (z_practical + z_edu - z_culture) / 3   -- culture 부호 반전
tf_score = (z_income + z_asset + z_price) / 3
jp_score = (z_price_cv + z_young) / 2              -- 2개 피처

-- MBTI 판정
E/I: ei_score >= 0 → E, < 0 → I
S/N: sn_score >= 0 → S, < 0 → N
T/F: tf_score >= 0 → T, < 0 → F
J/P: jp_score >= 0 → P, < 0 → J   -- jp_score 양수 = 변화(P)
```

## RICHGO 동→구 폴백 전략

RICHGO는 동 단위 데이터가 없는 경우 구 단위 평균으로 대체:

```sql
COALESCE(동_단위_값, 구_단위_평균)
```

실행 결과: RICHGO 매칭률 **100% (118/118)** — 폴백 포함.

## 검증 결과 (2026-04-09)

| 검증 항목 | 기준 | 결과 | 판정 |
|----------|------|------|------|
| 동 수 완전성 | ≥ 50 | 118동 | PASS |
| SPH 커버리지 | ≥ 40동 | 118동 | PASS |
| RICHGO 커버리지 | ≥ 40동 | 118동 (구 폴백) | PASS |
| 4축 NULL 비율 | < 10% | 전축 0.0% | PASS |
| MBTI 다양성 | ≥ 3종 | **16종 전체** | PASS |

## 실측 동 수

| 구 | 동 수 |
|----|------|
| 서초구 | 10 |
| 영등포구 | 34 |
| 중구 | 74 |
| **합계** | **118** |
