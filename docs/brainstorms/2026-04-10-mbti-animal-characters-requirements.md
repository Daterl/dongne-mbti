---
date: 2026-04-10
topic: mbti-animal-characters
---

# MBTI 16종 동물 캐릭터 제작

## Problem Frame

동네 MBTI 카드에 캐릭터 이미지가 없어서 시각적 임팩트와 인스타그램 공유 매력이 부족하다. MBTI별 동물 캐릭터를 추가해 "우리 동네 여우래 ㅋㅋ" 같은 바이럴 후크를 만든다.

## Requirements

**캐릭터 제작**

- R1. MBTI 16종 각각에 대응하는 동물 캐릭터 SVG를 인라인으로 제작한다
- R2. 각 동물은 MBTI 성격과 동네 4축 데이터 특성을 반영하는 소품/특징을 갖는다
- R3. SVG는 플랫/미니멀 스타일로 통일하고, MBTI_COLORS 팔레트의 색상을 기본 톤으로 사용한다

**16종 동물 매핑**

| MBTI | 동물 | 소품/특징 | 4축 근거 |
|------|------|----------|---------|
| INTJ | 여우 | 노트북 + 커피잔 | I조용 N문화 T고소득 J안정 |
| INTP | 올빼미 | 돋보기 + 카페라떼 | I조용 N문화 T고소득 P변화 |
| ENTJ | 도베르만 | 서류가방 + 넥타이 | E활발 N문화 T부유 J안정 |
| ENTP | 앵무새 | 메가폰 + 트렌디 선글라스 | E활발 N문화 T부유 P변동 |
| INFJ | 사슴 | 책 + 머플러 | I조용 N문화 F감성 J안정 |
| INFP | 토끼 | 꽃 화관 + 스케치북 | I조용 N문화 F감성 P자유 |
| ENFJ | 골든리트리버 | 도시락 + 태양 배지 | E활발 N문화 F감성 J커뮤니티 |
| ENFP | 길고양이 | 피어싱 + 카메라 | E활발 N문화 F감성 P변화 |
| ISTJ | 거북이 | 체크리스트 + 우산 | I조용 S실용 T경제 J매우안정 |
| ISFJ | 햄스터 | 앞치마 + 장바구니 | I조용 S실용 F따뜻 J안정 |
| ESTJ | 독수리 | 호루라기 + 완장 | E활발 S실용 T경제 J질서 |
| ESFJ | 말티즈 | 리본 + 선물상자 | E활발 S실용 F따뜻 J커뮤니티 |
| ISTP | 러시안블루 | 렌치 + 선글라스 | I조용 S실용 T합리 P유연 |
| ISFP | 아기 판다 | 팔레트 + 베레모 | I조용 S실용 F감성 P자유 |
| ESTP | 치타 | 운동화 + 번개 문양 | E유동인구 S실용 T경제 P역동 |
| ESFP | 수달 | 마이크 + 파티모자 | E활발 S실용 F감성 P흥 |

**앱 통합**

- R4. `app.py`에 `MBTI_ANIMALS` 딕셔너리로 SVG 코드를 관리한다
- R5. 탭1 MBTI 카드 상단(MBTI 타입 글자 위 또는 옆)에 캐릭터를 표시한다
- R6. `st.markdown(unsafe_allow_html=True)`로 렌더링한다 (SiS(Streamlit in Snowflake) 호환)

## Success Criteria

- 16종 캐릭터가 모두 카드에 표시되고 시각적으로 일관된 스타일
- SiS 환경에서 외부 네트워크 없이 정상 렌더링
- 인스타그램 스크린샷 시 캐릭터가 식별 가능한 크기와 선명도

## Scope Boundaries

- 동네(55개)별 개별 캐릭터는 만들지 않는다 (MBTI 16종 기준)
- 애니메이션/인터랙션은 포함하지 않는다
- 인스타그램 카드 별도 export 기능은 이번 스코프에서 제외한다

## Key Decisions

- **SVG 인라인 방식**: SiS 외부 네트워크 제약 무관, export 과정 불필요, 벡터라 해상도 무관하게 선명
- **동물 메타포**: 동물 습성과 동네 분위기를 연결해 바이럴 임팩트 극대화
- **MBTI 16종 기준**: 55개 동네별이 아닌 16 MBTI 기준으로 제작 (작업량 적고 MBTI 공유 아이덴티티 구축)
- **4축 데이터 기반 소품**: 일반 MBTI가 아닌 동네 MBTI 4축(활동성/라이프스타일/경제수준/안정성)에 맞춘 소품 선정

## Outstanding Questions

### Deferred to Planning

- [Affects R5][Technical] MBTI 카드 내 캐릭터 SVG 최적 사이즈와 배치 위치 결정
- [Affects R3][Technical] SVG 복잡도와 app.py 파일 크기 밸런스 — 전체 SVG 합산 500KB 초과 시 `constants.py`로 분리

## Next Steps

→ `/ce:plan` for structured implementation planning
