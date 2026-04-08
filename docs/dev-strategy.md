# 개발 전략

> 4/8 기준 | 남은 5일 | 크레딧 $40 | 2인 팀

---

## 도구 역할 분담

```
Claude Code (무료)          Cortex Code (크레딧 소비)       Snowflake 웹 (크레딧 소비)
─────────────────          ──────────────────────          ─────────────────────────
코드 작성/편집               데이터 탐색 (EDA)               Streamlit 앱 배포/실행
Git 관리                    Cortex AI 함수 테스트            데모 영상 촬영
문서화                      SQL 디버깅                       최종 검증
Semantic Model YAML 작성    테이블 생성/변환
```

**원칙**: Claude Code에서 최대한 작성 → Snowflake에서는 실행/검증만

---

## 크레딧 관리 ($40)

### 필수 설정 (Day 1 시작 전)

```sql
-- Warehouse 자동 중지 (1분 미사용 시)
ALTER WAREHOUSE COMPUTE_WH SET AUTO_SUSPEND = 60;
ALTER WAREHOUSE COMPUTE_WH SET AUTO_RESUME = TRUE;
ALTER WAREHOUSE COMPUTE_WH SET WAREHOUSE_SIZE = 'XSMALL';
```

### 예산 배분

| 기간 | 용도 | 예산 | 누적 |
|------|------|------|------|
| 4/8 | EDA + 테이블 설계 + JOIN 검증 | $8 | $8 |
| 4/9 | Cortex AI 파이프라인 (6개 기능 테스트) | $12 | $20 |
| 4/10 | Streamlit 앱 개발 + 디버깅 | $8 | $28 |
| 4/11 | 통합 테스트 + UI 폴리싱 | $6 | $34 |
| 4/12 | 데모 영상 촬영 + 최종 실행 | $4 | $38 |
| 여유분 | 예비 | $2 | $40 |

### 크레딧 절약 규칙

1. **Cortex AI 호출 전에 반드시 `LIMIT 10`으로 테스트** → 확인 후 전체 실행
2. **Warehouse를 안 쓸 때 수동 SUSPEND**: `ALTER WAREHOUSE COMPUTE_WH SUSPEND;`
3. **Claude Code에서 코드 완성 후 Snowflake에서 실행** (Snowflake에서 시행착오 X)
4. **크레딧 확인 명령** (매일 1회):
   ```sql
   SELECT * FROM SNOWFLAKE.ORGANIZATION_USAGE.REMAINING_BALANCE_DAILY;
   -- 또는
   SELECT SUM(CREDITS_USED) FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
   WHERE START_TIME >= DATEADD('day', -1, CURRENT_TIMESTAMP());
   ```

### 비용 감각

| 작업 | 예상 비용 |
|------|-----------|
| SELECT + LIMIT 100 | ~$0.003 |
| 복잡한 JOIN + 집계 | ~$0.01~0.05 |
| CORTEX.COMPLETE 1회 | ~$0.01~0.05 |
| CORTEX.COMPLETE 서울 전체 구(25개) | ~$0.5~1.0 |
| CORTEX.COMPLETE 전체 동(400+개) | ~$5~10 ⚠️ |
| Warehouse 1시간 방치 (XS) | ~$2 ⚠️ |
| Streamlit 앱 1시간 실행 | ~$2 |

> **가장 비싼 실수**: Warehouse 켜놓고 퇴근 ($2/hr × 8hr = $16 = 예산 40%)

---

## 개발 흐름

### Phase 1: 데이터 준비 (4/8)

```
Claude Code                              Snowflake
───────────                              ─────────
1. DONGNE_MASTER 테이블 SQL 작성    →    실행 + 검증
2. JOIN 키 매핑 SQL 작성            →    실행 + 결과 확인
3. EDA 쿼리 작성 (분포/NULL/이상치)  →    실행 + 결과 분석
4. 4축별 피처 확정                   →    샘플 데이터로 검증
```

### Phase 2: Cortex AI 파이프라인 (4/9)

```
Claude Code                              Snowflake
───────────                              ─────────
1. AI_CLASSIFY SQL 작성             →    LIMIT 10으로 테스트 → 전체 실행
2. AI_COMPLETE 프롬프트 설계         →    LIMIT 5로 테스트 → 전체 실행
3. AI_SENTIMENT SQL 작성            →    LIMIT 10으로 테스트
4. Semantic Model YAML 작성         →    Cortex Analyst 테스트
5. Cortex Search 인덱스 SQL         →    생성 + 검색 테스트
6. Cortex Agent 설정                →    3턴 대화 테스트
```

**핵심**: 6개 기능 "모두 동작" 우선. 품질 튜닝은 나중에.

### Phase 3: Streamlit UI (4/10)

```
Claude Code                              Snowflake
───────────                              ─────────
1. streamlit_app.py 전체 작성        →    Streamlit in Snowflake에 업로드
2. 커스텀 HTML/CSS 컴포넌트 작성     →    렌더링 확인
3. 탭 1/2/3 통합                    →    동작 확인
```

**전략**: Claude Code에서 앱 코드를 90% 완성한 후 Snowflake에 올려서 디버깅

### Phase 4: 테스트 + 제출 (4/11~12)

```
4/11: E2E 테스트 + 버그 수정 + UI 폴리싱
4/12: 데모 영상(QuickTime) + PPT + ZIP → 제출
```

---

## Cortex AI 호출 패턴

### 안전한 패턴 (크레딧 절약)

```sql
-- 1. 항상 LIMIT으로 먼저 테스트
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'claude-3-5-sonnet',
    CONCAT('동네 성격을 분석해줘: ', SGG, ' ', EMD)
) AS mbti_summary
FROM DONGNE_MASTER
LIMIT 3;  -- ✅ 먼저 3건만

-- 2. 결과 확인 후 전체 실행 + 결과 저장
CREATE TABLE DONGNE_MBTI_RESULT AS
SELECT *, SNOWFLAKE.CORTEX.COMPLETE(...) AS mbti_summary
FROM DONGNE_MASTER;  -- 한 번만 실행하고 결과 테이블에 저장

-- 3. 이후에는 결과 테이블만 조회 (AI 재호출 없음)
SELECT * FROM DONGNE_MBTI_RESULT WHERE SGG = '마포구';
```

### 위험한 패턴 (크레딧 낭비)

```sql
-- ❌ Streamlit에서 매번 AI 호출
-- 사용자가 동네 선택할 때마다 COMPLETE 호출 → 크레딧 폭탄
result = session.sql("SELECT CORTEX.COMPLETE(...)")  -- 매 클릭마다 $0.05

-- ✅ 대신: 미리 계산된 결과 테이블에서 조회
result = session.sql("SELECT * FROM DONGNE_MBTI_RESULT WHERE ...")  -- $0.003
```

**원칙**: Cortex AI는 **배치로 한 번 실행 → 결과 저장 → 이후 조회만**

> 예외: 탭 2 자연어 찾기는 실시간 Agent 호출 필요 (사용자 질의가 매번 다르므로)

---

## 구 단위 vs 동 단위

크레딧 제약 때문에 분석 단위를 전략적으로 선택:

| 단위 | 수량 | Cortex AI 비용 | 결정 |
|------|------|----------------|------|
| 서울 구 단위 | ~25개 | ~$1 | ✅ 기본 분석 단위 |
| 서울 동 단위 | ~400+개 | ~$10+ | ⚠️ 시간/크레딧 여유 시만 |

**전략**: 구 단위로 MVP 완성 → 여유 있으면 동 단위로 확장

---

## 파일 구조 (예상)

```
dongne-mbti/
├── docs/                          # 문서 (현재)
├── sql/
│   ├── 01_create_master.sql       # 동네 마스터 테이블
│   ├── 02_eda.sql                 # EDA 쿼리
│   ├── 03_mbti_classify.sql       # AI_CLASSIFY 배치
│   ├── 04_mbti_complete.sql       # AI_COMPLETE 배치
│   ├── 05_sentiment.sql           # AI_SENTIMENT 배치
│   ├── 06_search_index.sql        # Cortex Search 인덱스
│   └── 07_agent_setup.sql         # Cortex Agent 설정
├── semantic_model/
│   └── dongne.yaml                # Cortex Analyst Semantic Model
├── streamlit/
│   ├── streamlit_app.py           # 메인 앱
│   ├── components/                # 커스텀 HTML/CSS
│   └── utils.py                   # 헬퍼 함수
└── README.md
```
