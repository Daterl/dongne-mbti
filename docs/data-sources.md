# 데이터 소스 및 Cortex AI 활용 매핑

## Marketplace 데이터

### 리치고 (Richgo)
- 서울 아파트 시세 (2021~2026)
- 지하철역 거리/이용 통계
- 인구 이동 데이터

### SPH
- SKT 유동인구 (5년)
- KCB 자산/소득
- 신한카드 소비내역 (2021~2025)

### 아정당 (AJD)
- 이사/이동 추정 데이터
- 렌탈 데이터
- 고객 세그먼트

### 넥스트레이드 (NextTrade)
- 주식 시장 데이터 (부가 경제지표)

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

## Snowflake 계정 설정

- **리전**: AWS Seoul 또는 US West (Oregon)
- **계정**: 무료 30일 트라이얼 (만료 시 신규 생성)
- **콘솔**: https://app.snowflake.com
