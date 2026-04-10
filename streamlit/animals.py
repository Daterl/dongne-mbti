"""
MBTI 16종 동물 캐릭터 SVG + 이름 매핑
플랫/미니멀 스타일, viewBox 80x80, fill white 계열
"""

# MBTI별 동물 이름 (한글)
MBTI_ANIMAL_NAMES = {
    "INTJ": "여우",
    "INTP": "올빼미",
    "ENTJ": "도베르만",
    "ENTP": "앵무새",
    "INFJ": "사슴",
    "INFP": "토끼",
    "ENFJ": "골든리트리버",
    "ENFP": "길고양이",
    "ISTJ": "거북이",
    "ISFJ": "햄스터",
    "ESTJ": "독수리",
    "ESFJ": "말티즈",
    "ISTP": "러시안블루",
    "ISFP": "아기 판다",
    "ESTP": "치타",
    "ESFP": "수달",
}

# MBTI별 동물 캐릭터 SVG (80x80, 흰색/반투명)
MBTI_ANIMALS = {
    # ── INTJ: 여우 (노트북 + 커피잔) ──
    "INTJ": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 귀 -->
  <polygon points="22,12 30,30 14,30" fill="rgba(255,255,255,0.85)"/>
  <polygon points="58,12 66,30 50,30" fill="rgba(255,255,255,0.85)"/>
  <!-- 얼굴 -->
  <ellipse cx="40" cy="38" rx="18" ry="16" fill="white"/>
  <!-- 눈 -->
  <circle cx="33" cy="35" r="2.5" fill="#333"/>
  <circle cx="47" cy="35" r="2.5" fill="#333"/>
  <!-- 코 -->
  <polygon points="40,40 37,43 43,43" fill="#333"/>
  <!-- 노트북 -->
  <rect x="25" y="58" width="16" height="10" rx="1" fill="rgba(255,255,255,0.6)"/>
  <rect x="25" y="56" width="16" height="3" rx="1" fill="rgba(255,255,255,0.8)"/>
  <!-- 커피잔 -->
  <rect x="48" y="60" width="8" height="8" rx="1" fill="rgba(255,255,255,0.7)"/>
  <path d="M56,63 Q60,63 60,67 Q60,68 56,68" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.5"/>
  <!-- 커피 김 -->
  <path d="M50,57 Q51,54 52,57" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
  <path d="M53,56 Q54,53 55,56" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
</svg>''',

    # ── INTP: 올빼미 (돋보기 + 카페라떼) ──
    "INTP": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 귀 깃털 -->
  <polygon points="24,10 28,24 20,24" fill="rgba(255,255,255,0.7)"/>
  <polygon points="56,10 60,24 52,24" fill="rgba(255,255,255,0.7)"/>
  <!-- 몸통 -->
  <ellipse cx="40" cy="40" rx="20" ry="18" fill="white"/>
  <!-- 큰 눈 테두리 -->
  <circle cx="32" cy="36" r="8" fill="rgba(255,255,255,0.3)" stroke="white" stroke-width="1.5"/>
  <circle cx="48" cy="36" r="8" fill="rgba(255,255,255,0.3)" stroke="white" stroke-width="1.5"/>
  <!-- 눈동자 -->
  <circle cx="32" cy="36" r="3" fill="#333"/>
  <circle cx="48" cy="36" r="3" fill="#333"/>
  <!-- 부리 -->
  <polygon points="40,42 37,46 43,46" fill="#F0C040"/>
  <!-- 돋보기 -->
  <circle cx="28" cy="66" r="5" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="1.5"/>
  <line x1="32" y1="70" x2="36" y2="74" stroke="rgba(255,255,255,0.8)" stroke-width="1.5"/>
  <!-- 카페라떼 -->
  <rect x="46" y="62" width="8" height="10" rx="1" fill="rgba(255,255,255,0.6)"/>
  <ellipse cx="50" cy="62" rx="4" ry="1.5" fill="rgba(255,255,255,0.8)"/>
</svg>''',

    # ── ENTJ: 도베르만 (서류가방 + 넥타이) ──
    "ENTJ": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 귀 -->
  <polygon points="20,8 28,26 14,22" fill="rgba(255,255,255,0.85)"/>
  <polygon points="60,8 66,22 52,26" fill="rgba(255,255,255,0.85)"/>
  <!-- 얼굴 -->
  <ellipse cx="40" cy="32" rx="16" ry="14" fill="white"/>
  <!-- 주둥이 -->
  <ellipse cx="40" cy="40" rx="8" ry="5" fill="rgba(255,255,255,0.7)"/>
  <!-- 눈 (날카로운) -->
  <ellipse cx="33" cy="30" rx="3" ry="2" fill="#333"/>
  <ellipse cx="47" cy="30" r="3" ry="2" fill="#333"/>
  <!-- 코 -->
  <ellipse cx="40" cy="38" rx="3" ry="2" fill="#333"/>
  <!-- 넥타이 -->
  <polygon points="40,48 36,56 40,54 44,56" fill="rgba(255,255,255,0.9)"/>
  <!-- 서류가방 -->
  <rect x="24" y="62" width="16" height="11" rx="2" fill="rgba(255,255,255,0.7)"/>
  <rect x="29" y="60" width="6" height="3" rx="1" fill="rgba(255,255,255,0.5)"/>
  <line x1="24" y1="67" x2="40" y2="67" stroke="rgba(255,255,255,0.4)" stroke-width="0.8"/>
</svg>''',

    # ── ENTP: 앵무새 (메가폰 + 선글라스) ──
    "ENTP": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 머리 깃털 -->
  <path d="M40,8 Q44,4 42,14" fill="rgba(255,255,255,0.7)"/>
  <path d="M44,10 Q48,5 45,16" fill="rgba(255,255,255,0.6)"/>
  <path d="M36,10 Q32,5 35,16" fill="rgba(255,255,255,0.6)"/>
  <!-- 몸통 -->
  <ellipse cx="40" cy="36" rx="16" ry="16" fill="white"/>
  <!-- 선글라스 -->
  <rect x="26" y="30" width="11" height="7" rx="2" fill="rgba(0,0,0,0.3)"/>
  <rect x="43" y="30" width="11" height="7" rx="2" fill="rgba(0,0,0,0.3)"/>
  <line x1="37" y1="33" x2="43" y2="33" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
  <!-- 부리 -->
  <path d="M36,40 L40,46 L44,40 Z" fill="#F0C040"/>
  <!-- 메가폰 -->
  <polygon points="50,58 66,52 66,68 50,64" fill="rgba(255,255,255,0.7)"/>
  <rect x="46" y="58" width="5" height="6" rx="1" fill="rgba(255,255,255,0.8)"/>
</svg>''',

    # ── INFJ: 사슴 (책 + 머플러) ──
    "INFJ": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 뿔 -->
  <path d="M28,18 L24,6 M24,6 L20,10 M24,6 L28,10" stroke="rgba(255,255,255,0.7)" stroke-width="1.5" fill="none"/>
  <path d="M52,18 L56,6 M56,6 L60,10 M56,6 L52,10" stroke="rgba(255,255,255,0.7)" stroke-width="1.5" fill="none"/>
  <!-- 귀 -->
  <ellipse cx="24" cy="24" rx="5" ry="8" fill="rgba(255,255,255,0.6)" transform="rotate(-20,24,24)"/>
  <ellipse cx="56" cy="24" rx="5" ry="8" fill="rgba(255,255,255,0.6)" transform="rotate(20,56,24)"/>
  <!-- 얼굴 -->
  <ellipse cx="40" cy="34" rx="14" ry="14" fill="white"/>
  <!-- 눈 (온화한) -->
  <ellipse cx="34" cy="32" rx="2.5" ry="3" fill="#333"/>
  <circle cx="33" cy="31" r="0.8" fill="white"/>
  <ellipse cx="46" cy="32" rx="2.5" ry="3" fill="#333"/>
  <circle cx="45" cy="31" r="0.8" fill="white"/>
  <!-- 코 -->
  <ellipse cx="40" cy="39" rx="2" ry="1.5" fill="#333"/>
  <!-- 머플러 -->
  <path d="M26,48 Q40,52 54,48" stroke="rgba(255,255,255,0.8)" stroke-width="3" fill="none"/>
  <rect x="50" y="48" width="4" height="10" rx="1" fill="rgba(255,255,255,0.7)"/>
  <!-- 책 -->
  <rect x="22" y="62" width="12" height="10" rx="1" fill="rgba(255,255,255,0.7)"/>
  <line x1="28" y1="62" x2="28" y2="72" stroke="rgba(255,255,255,0.4)" stroke-width="0.8"/>
</svg>''',

    # ── INFP: 토끼 (꽃 화관 + 스케치북) ──
    "INFP": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 귀 -->
  <ellipse cx="32" cy="14" rx="5" ry="14" fill="white"/>
  <ellipse cx="32" cy="14" rx="2.5" ry="10" fill="rgba(255,255,255,0.5)"/>
  <ellipse cx="48" cy="14" rx="5" ry="14" fill="white"/>
  <ellipse cx="48" cy="14" rx="2.5" ry="10" fill="rgba(255,255,255,0.5)"/>
  <!-- 꽃 화관 -->
  <circle cx="28" cy="22" r="3" fill="rgba(255,200,200,0.8)"/>
  <circle cx="40" cy="20" r="3" fill="rgba(255,220,180,0.8)"/>
  <circle cx="52" cy="22" r="3" fill="rgba(200,220,255,0.8)"/>
  <!-- 얼굴 -->
  <circle cx="40" cy="38" r="14" fill="white"/>
  <!-- 눈 (동그란 몽상가) -->
  <circle cx="34" cy="36" r="3" fill="#333"/>
  <circle cx="33" cy="35" r="1" fill="white"/>
  <circle cx="46" cy="36" r="3" fill="#333"/>
  <circle cx="45" cy="35" r="1" fill="white"/>
  <!-- 코 + 입 -->
  <circle cx="40" cy="42" r="1.5" fill="rgba(255,180,180,0.8)"/>
  <path d="M38,44 Q40,46 42,44" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="0.8"/>
  <!-- 스케치북 -->
  <rect x="24" y="58" width="14" height="16" rx="1" fill="rgba(255,255,255,0.7)"/>
  <line x1="28" y1="62" x2="34" y2="62" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
  <line x1="28" y1="65" x2="33" y2="65" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
  <line x1="28" y1="68" x2="32" y2="68" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
</svg>''',

    # ── ENFJ: 골든리트리버 (도시락 + 태양 배지) ──
    "ENFJ": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 귀 -->
  <ellipse cx="22" cy="28" rx="8" ry="12" fill="rgba(255,255,255,0.6)" transform="rotate(-10,22,28)"/>
  <ellipse cx="58" cy="28" rx="8" ry="12" fill="rgba(255,255,255,0.6)" transform="rotate(10,58,28)"/>
  <!-- 얼굴 -->
  <circle cx="40" cy="34" r="16" fill="white"/>
  <!-- 눈 (따뜻한 미소) -->
  <circle cx="33" cy="32" r="2.5" fill="#333"/>
  <circle cx="47" cy="32" r="2.5" fill="#333"/>
  <!-- 코 -->
  <ellipse cx="40" cy="38" rx="3" ry="2" fill="#333"/>
  <!-- 웃는 입 -->
  <path d="M34,42 Q40,48 46,42" fill="none" stroke="#333" stroke-width="1.2"/>
  <!-- 혀 -->
  <ellipse cx="40" cy="46" rx="3" ry="2" fill="rgba(255,180,180,0.7)"/>
  <!-- 태양 배지 -->
  <circle cx="56" cy="56" r="5" fill="rgba(255,220,100,0.8)"/>
  <line x1="56" y1="49" x2="56" y2="51" stroke="rgba(255,220,100,0.6)" stroke-width="1"/>
  <line x1="56" y1="61" x2="56" y2="63" stroke="rgba(255,220,100,0.6)" stroke-width="1"/>
  <line x1="49" y1="56" x2="51" y2="56" stroke="rgba(255,220,100,0.6)" stroke-width="1"/>
  <line x1="61" y1="56" x2="63" y2="56" stroke="rgba(255,220,100,0.6)" stroke-width="1"/>
  <!-- 도시락 -->
  <rect x="22" y="60" width="14" height="10" rx="2" fill="rgba(255,255,255,0.7)"/>
  <line x1="22" y1="65" x2="36" y2="65" stroke="rgba(255,255,255,0.4)" stroke-width="0.8"/>
</svg>''',

    # ── ENFP: 길고양이 (피어싱 + 카메라) ──
    "ENFP": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 귀 -->
  <polygon points="24,10 32,28 16,26" fill="rgba(255,255,255,0.85)"/>
  <polygon points="56,10 64,26 48,28" fill="rgba(255,255,255,0.85)"/>
  <!-- 피어싱 (왼쪽 귀) -->
  <circle cx="19" cy="20" r="1.5" fill="rgba(255,220,100,0.9)"/>
  <!-- 얼굴 -->
  <ellipse cx="40" cy="36" rx="16" ry="14" fill="white"/>
  <!-- 눈 (장난스러운) -->
  <ellipse cx="33" cy="33" rx="3" ry="3.5" fill="#333"/>
  <circle cx="32" cy="32" r="1" fill="white"/>
  <ellipse cx="47" cy="33" rx="3" ry="3.5" fill="#333"/>
  <circle cx="46" cy="32" r="1" fill="white"/>
  <!-- 코 -->
  <polygon points="40,38 38,40 42,40" fill="rgba(255,180,180,0.8)"/>
  <!-- 수염 -->
  <line x1="22" y1="38" x2="34" y2="39" stroke="rgba(255,255,255,0.5)" stroke-width="0.6"/>
  <line x1="22" y1="42" x2="34" y2="41" stroke="rgba(255,255,255,0.5)" stroke-width="0.6"/>
  <line x1="58" y1="38" x2="46" y2="39" stroke="rgba(255,255,255,0.5)" stroke-width="0.6"/>
  <line x1="58" y1="42" x2="46" y2="41" stroke="rgba(255,255,255,0.5)" stroke-width="0.6"/>
  <!-- 카메라 -->
  <rect x="46" y="58" width="14" height="10" rx="2" fill="rgba(255,255,255,0.7)"/>
  <circle cx="53" cy="63" r="3" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
  <rect x="50" y="56" width="4" height="3" rx="1" fill="rgba(255,255,255,0.5)"/>
</svg>''',

    # ── ISTJ: 거북이 (체크리스트 + 우산) ──
    "ISTJ": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 등딱지 -->
  <ellipse cx="40" cy="38" rx="20" ry="16" fill="rgba(255,255,255,0.7)"/>
  <!-- 등딱지 무늬 -->
  <path d="M30,30 L40,38 L50,30" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <path d="M26,40 L40,38 L54,40" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <!-- 머리 -->
  <circle cx="40" cy="20" r="10" fill="white"/>
  <!-- 눈 (진지한) -->
  <circle cx="36" cy="19" r="2" fill="#333"/>
  <circle cx="44" cy="19" r="2" fill="#333"/>
  <!-- 입 (일자) -->
  <line x1="37" y1="24" x2="43" y2="24" stroke="#333" stroke-width="1"/>
  <!-- 다리 -->
  <ellipse cx="26" cy="50" rx="4" ry="3" fill="rgba(255,255,255,0.6)"/>
  <ellipse cx="54" cy="50" rx="4" ry="3" fill="rgba(255,255,255,0.6)"/>
  <!-- 체크리스트 -->
  <rect x="18" y="58" width="12" height="16" rx="1" fill="rgba(255,255,255,0.7)"/>
  <line x1="21" y1="62" x2="27" y2="62" stroke="rgba(255,255,255,0.4)" stroke-width="0.6"/>
  <line x1="21" y1="65" x2="27" y2="65" stroke="rgba(255,255,255,0.4)" stroke-width="0.6"/>
  <line x1="21" y1="68" x2="27" y2="68" stroke="rgba(255,255,255,0.4)" stroke-width="0.6"/>
  <path d="M20,61 L21,62 L23,60" stroke="rgba(255,255,255,0.5)" stroke-width="0.8" fill="none"/>
  <path d="M20,64 L21,65 L23,63" stroke="rgba(255,255,255,0.5)" stroke-width="0.8" fill="none"/>
  <!-- 우산 -->
  <path d="M56,56 Q56,50 62,50 Q68,50 68,56" fill="rgba(255,255,255,0.6)"/>
  <line x1="62" y1="50" x2="62" y2="72" stroke="rgba(255,255,255,0.7)" stroke-width="1"/>
  <path d="M62,72 Q60,74 58,72" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1"/>
</svg>''',

    # ── ISFJ: 햄스터 (앞치마 + 장바구니) ──
    "ISFJ": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 귀 -->
  <circle cx="26" cy="18" r="7" fill="rgba(255,255,255,0.7)"/>
  <circle cx="26" cy="18" r="4" fill="rgba(255,255,255,0.4)"/>
  <circle cx="54" cy="18" r="7" fill="rgba(255,255,255,0.7)"/>
  <circle cx="54" cy="18" r="4" fill="rgba(255,255,255,0.4)"/>
  <!-- 얼굴 -->
  <circle cx="40" cy="32" r="16" fill="white"/>
  <!-- 볼 -->
  <circle cx="28" cy="36" r="5" fill="rgba(255,200,200,0.3)"/>
  <circle cx="52" cy="36" r="5" fill="rgba(255,200,200,0.3)"/>
  <!-- 눈 -->
  <circle cx="34" cy="30" r="2.5" fill="#333"/>
  <circle cx="46" cy="30" r="2.5" fill="#333"/>
  <!-- 코 -->
  <circle cx="40" cy="36" r="1.5" fill="rgba(255,180,180,0.8)"/>
  <!-- 입 -->
  <path d="M37,39 Q40,42 43,39" fill="none" stroke="#333" stroke-width="0.8"/>
  <!-- 앞치마 -->
  <path d="M30,48 L30,58 Q40,62 50,58 L50,48 Z" fill="rgba(255,255,255,0.5)"/>
  <path d="M34,48 Q40,46 46,48" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1"/>
  <!-- 장바구니 -->
  <path d="M52,60 L48,72 L66,72 L62,60 Z" fill="rgba(255,255,255,0.6)"/>
  <path d="M50,60 Q57,56 64,60" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1"/>
  <line x1="52" y1="64" x2="62" y2="64" stroke="rgba(255,255,255,0.3)" stroke-width="0.5"/>
  <line x1="51" y1="68" x2="63" y2="68" stroke="rgba(255,255,255,0.3)" stroke-width="0.5"/>
</svg>''',

    # ── ESTJ: 독수리 (호루라기 + 완장) ──
    "ESTJ": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 몸통 -->
  <ellipse cx="40" cy="38" rx="16" ry="18" fill="white"/>
  <!-- 날개 -->
  <path d="M20,30 Q16,40 22,50" stroke="rgba(255,255,255,0.6)" stroke-width="2" fill="rgba(255,255,255,0.3)"/>
  <path d="M60,30 Q64,40 58,50" stroke="rgba(255,255,255,0.6)" stroke-width="2" fill="rgba(255,255,255,0.3)"/>
  <!-- 머리 -->
  <circle cx="40" cy="20" r="10" fill="white"/>
  <!-- 눈 (날카로운) -->
  <line x1="33" y1="17" x2="37" y2="19" stroke="#333" stroke-width="1.2"/>
  <circle cx="35" cy="19" r="2" fill="#333"/>
  <line x1="47" y1="17" x2="43" y2="19" stroke="#333" stroke-width="1.2"/>
  <circle cx="45" cy="19" r="2" fill="#333"/>
  <!-- 부리 -->
  <path d="M38,24 L40,30 L42,24 Z" fill="#F0C040"/>
  <!-- 완장 -->
  <rect x="18" y="34" width="6" height="10" rx="1" fill="rgba(255,220,100,0.7)"/>
  <!-- 호루라기 -->
  <circle cx="56" cy="62" r="4" fill="rgba(255,255,255,0.7)"/>
  <rect x="56" y="60" width="10" height="4" rx="1" fill="rgba(255,255,255,0.6)"/>
  <line x1="50" y1="58" x2="56" y2="62" stroke="rgba(255,255,255,0.5)" stroke-width="1"/>
</svg>''',

    # ── ESFJ: 말티즈 (리본 + 선물상자) ──
    "ESFJ": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 털 (복슬복슬) -->
  <circle cx="26" cy="28" r="8" fill="rgba(255,255,255,0.5)"/>
  <circle cx="54" cy="28" r="8" fill="rgba(255,255,255,0.5)"/>
  <circle cx="30" cy="22" r="6" fill="rgba(255,255,255,0.5)"/>
  <circle cx="50" cy="22" r="6" fill="rgba(255,255,255,0.5)"/>
  <!-- 얼굴 -->
  <circle cx="40" cy="32" r="14" fill="white"/>
  <!-- 리본 -->
  <path d="M36,16 Q40,20 44,16" fill="rgba(255,180,200,0.8)"/>
  <path d="M36,24 Q40,20 44,24" fill="rgba(255,180,200,0.8)"/>
  <circle cx="40" cy="20" r="2" fill="rgba(255,150,180,0.9)"/>
  <!-- 눈 -->
  <circle cx="34" cy="30" r="2.5" fill="#333"/>
  <circle cx="46" cy="30" r="2.5" fill="#333"/>
  <!-- 코 -->
  <circle cx="40" cy="36" r="2" fill="#333"/>
  <!-- 웃는 입 -->
  <path d="M36,40 Q40,44 44,40" fill="none" stroke="#333" stroke-width="1"/>
  <!-- 선물상자 -->
  <rect x="48" y="56" width="14" height="14" rx="2" fill="rgba(255,255,255,0.7)"/>
  <line x1="55" y1="56" x2="55" y2="70" stroke="rgba(255,180,200,0.6)" stroke-width="1.5"/>
  <line x1="48" y1="63" x2="62" y2="63" stroke="rgba(255,180,200,0.6)" stroke-width="1.5"/>
  <path d="M52,56 Q55,52 58,56" fill="none" stroke="rgba(255,180,200,0.7)" stroke-width="1"/>
</svg>''',

    # ── ISTP: 러시안블루 (렌치 + 선글라스) ──
    "ISTP": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 귀 -->
  <polygon points="24,10 32,26 16,24" fill="rgba(255,255,255,0.85)"/>
  <polygon points="56,10 64,24 48,26" fill="rgba(255,255,255,0.85)"/>
  <!-- 얼굴 -->
  <ellipse cx="40" cy="34" rx="16" ry="14" fill="white"/>
  <!-- 선글라스 -->
  <rect x="26" y="28" width="11" height="8" rx="2" fill="rgba(0,0,0,0.35)"/>
  <rect x="43" y="28" width="11" height="8" rx="2" fill="rgba(0,0,0,0.35)"/>
  <line x1="37" y1="32" x2="43" y2="32" stroke="rgba(255,255,255,0.6)" stroke-width="1"/>
  <!-- 코 -->
  <polygon points="40,38 38,40 42,40" fill="rgba(255,180,180,0.7)"/>
  <!-- 수염 -->
  <line x1="22" y1="38" x2="34" y2="38" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
  <line x1="22" y1="41" x2="34" y2="40" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
  <line x1="58" y1="38" x2="46" y2="38" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
  <line x1="58" y1="41" x2="46" y2="40" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
  <!-- 렌치 -->
  <line x1="50" y1="56" x2="64" y2="70" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>
  <path d="M48,54 Q50,52 52,54 L51,56 L49,56 Z" fill="rgba(255,255,255,0.8)"/>
  <path d="M62,68 Q66,64 68,68 Q68,72 64,72 Z" fill="rgba(255,255,255,0.8)"/>
</svg>''',

    # ── ISFP: 아기 판다 (팔레트 + 베레모) ──
    "ISFP": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 베레모 -->
  <ellipse cx="40" cy="16" rx="14" ry="5" fill="rgba(255,255,255,0.7)"/>
  <path d="M26,16 Q28,8 40,6 Q52,8 54,16" fill="rgba(255,255,255,0.6)"/>
  <circle cx="40" cy="8" r="2" fill="rgba(255,255,255,0.8)"/>
  <!-- 귀 (검은 패치) -->
  <circle cx="26" cy="20" r="7" fill="rgba(255,255,255,0.4)"/>
  <circle cx="54" cy="20" r="7" fill="rgba(255,255,255,0.4)"/>
  <!-- 얼굴 -->
  <circle cx="40" cy="32" r="14" fill="white"/>
  <!-- 눈 패치 -->
  <ellipse cx="33" cy="30" rx="6" ry="5" fill="rgba(0,0,0,0.15)"/>
  <ellipse cx="47" cy="30" rx="6" ry="5" fill="rgba(0,0,0,0.15)"/>
  <!-- 눈 -->
  <circle cx="33" cy="30" r="2.5" fill="#333"/>
  <circle cx="32" cy="29" r="0.8" fill="white"/>
  <circle cx="47" cy="30" r="2.5" fill="#333"/>
  <circle cx="46" cy="29" r="0.8" fill="white"/>
  <!-- 코 -->
  <ellipse cx="40" cy="37" rx="2" ry="1.5" fill="#333"/>
  <!-- 팔레트 -->
  <ellipse cx="28" cy="64" rx="10" ry="7" fill="rgba(255,255,255,0.6)"/>
  <circle cx="22" cy="62" r="2" fill="rgba(255,100,100,0.6)"/>
  <circle cx="26" cy="58" r="2" fill="rgba(100,200,255,0.6)"/>
  <circle cx="32" cy="58" r="2" fill="rgba(255,220,100,0.6)"/>
  <circle cx="35" cy="62" r="2" fill="rgba(100,255,150,0.6)"/>
  <circle cx="28" cy="68" r="2.5" fill="rgba(255,255,255,0.3)"/>
</svg>''',

    # ── ESTP: 치타 (운동화 + 번개 문양) ──
    "ESTP": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 귀 -->
  <ellipse cx="28" cy="14" rx="6" ry="8" fill="rgba(255,255,255,0.8)"/>
  <ellipse cx="52" cy="14" rx="6" ry="8" fill="rgba(255,255,255,0.8)"/>
  <!-- 얼굴 -->
  <ellipse cx="40" cy="32" rx="16" ry="14" fill="white"/>
  <!-- 점 무늬 -->
  <circle cx="24" cy="28" r="1.2" fill="rgba(255,255,255,0.3)"/>
  <circle cx="28" cy="24" r="1" fill="rgba(255,255,255,0.3)"/>
  <circle cx="56" cy="28" r="1.2" fill="rgba(255,255,255,0.3)"/>
  <circle cx="52" cy="24" r="1" fill="rgba(255,255,255,0.3)"/>
  <!-- 눈 (역동적) -->
  <ellipse cx="33" cy="30" rx="3" ry="2.5" fill="#333"/>
  <ellipse cx="47" cy="30" rx="3" ry="2.5" fill="#333"/>
  <!-- 눈물선 -->
  <path d="M30,33 L28,38" stroke="#333" stroke-width="1"/>
  <path d="M50,33 L52,38" stroke="#333" stroke-width="1"/>
  <!-- 코 -->
  <polygon points="40,36 38,38 42,38" fill="#333"/>
  <!-- 번개 문양 -->
  <polygon points="56,52 52,60 56,60 52,70 60,58 56,58 60,52" fill="rgba(255,220,100,0.8)"/>
  <!-- 운동화 -->
  <path d="M20,64 L18,72 L32,72 L32,68 L24,68 L26,64 Z" fill="rgba(255,255,255,0.7)"/>
  <line x1="22" y1="68" x2="22" y2="72" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
  <line x1="26" y1="68" x2="26" y2="72" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
</svg>''',

    # ── ESFP: 수달 (마이크 + 파티모자) ──
    "ESFP": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <!-- 파티모자 -->
  <polygon points="40,2 32,18 48,18" fill="rgba(255,220,100,0.7)"/>
  <circle cx="40" cy="2" r="2" fill="rgba(255,150,150,0.8)"/>
  <line x1="34" y1="12" x2="46" y2="12" stroke="rgba(255,255,255,0.4)" stroke-width="0.6"/>
  <!-- 귀 -->
  <circle cx="24" cy="22" r="5" fill="rgba(255,255,255,0.6)"/>
  <circle cx="56" cy="22" r="5" fill="rgba(255,255,255,0.6)"/>
  <!-- 얼굴 -->
  <ellipse cx="40" cy="32" rx="16" ry="14" fill="white"/>
  <!-- 눈 (신나는) -->
  <path d="M30,30 Q33,26 36,30" stroke="#333" stroke-width="1.5" fill="none"/>
  <path d="M44,30 Q47,26 50,30" stroke="#333" stroke-width="1.5" fill="none"/>
  <!-- 코 -->
  <ellipse cx="40" cy="35" rx="3" ry="2" fill="#333"/>
  <!-- 큰 웃음 -->
  <path d="M32,39 Q40,48 48,39" fill="none" stroke="#333" stroke-width="1.2"/>
  <!-- 수염 -->
  <line x1="24" y1="36" x2="34" y2="36" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
  <line x1="56" y1="36" x2="46" y2="36" stroke="rgba(255,255,255,0.4)" stroke-width="0.5"/>
  <!-- 마이크 -->
  <circle cx="58" cy="58" r="5" fill="rgba(255,255,255,0.7)"/>
  <line x1="58" y1="63" x2="58" y2="74" stroke="rgba(255,255,255,0.6)" stroke-width="2"/>
  <rect x="55" y="55" width="6" height="6" rx="3" fill="rgba(255,255,255,0.5)"/>
</svg>''',
}
