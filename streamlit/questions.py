"""
동네 MBTI 성향 테스트 — 8개 시나리오 질문 + 다축 가중치 스코어링

각 질문은 4개 선택지를 가지며, 각 선택지는 E/I·S/N·T/F·J/P 축에
서로 다른 가중치로 기여한다. 사용자는 "라이프스타일 시나리오"를 고르지만,
실제로는 여러 축이 동시에 측정되어 결과를 예측할 수 없다.

축 방향 규약 (동네 z-score와 동일):
  EI: 양수 = E(외향/활동), 음수 = I(내향/조용)
  SN: 양수 = S(실용/가정), 음수 = N(문화/트렌디)
  TF: 양수 = T(부유/투자), 음수 = F(서민/감성)
  JP: 양수 = P(변화/유동), 음수 = J(안정/정착)
"""

from math import sqrt

# ── 8개 질문 정의 ────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "id": 1,
        "emoji": "🏙️",
        "title": "동네 첫인상",
        "question": "새 동네에 이사 왔어요. 창문을 열면 어떤 풍경이 보이면 좋겠어요?",
        "options": [
            "저녁이면 불빛 가득한 상점가, 오가는 사람들의 활기",
            "아이들 놀이터가 있는 공원, 잘 정돈된 아파트 단지",
            "개성 있는 카페와 작은 갤러리가 늘어선 골목",
            "가로수 심어진 조용한 주택가, 밤이면 고요한 거리",
        ],
        "weights": [
            {"EI": 0.5, "SN": 0.0, "TF": 0.0, "JP": 0.2},
            {"EI": -0.3, "SN": 0.4, "TF": 0.0, "JP": -0.4},
            {"EI": 0.2, "SN": -0.5, "TF": 0.0, "JP": 0.3},
            {"EI": -0.6, "SN": 0.0, "TF": 0.0, "JP": -0.3},
        ],
    },
    {
        "id": 2,
        "emoji": "🍽️",
        "title": "저녁 식사",
        "question": "퇴근길, 오늘 저녁은 어떻게 할까요?",
        "options": [
            "동네 단골 식당에서 든든하게 — 맛있고 가성비가 최고",
            "배달앱으로 새로운 맛집 탐색 — 집에서 편하게",
            "동네 와인 바에서 분위기 있는 한 잔",
            "직접 요리 — 재료는 백화점 식품관이나 유기농 마켓에서",
        ],
        "weights": [
            {"EI": 0.2, "SN": 0.5, "TF": -0.3, "JP": 0.0},
            {"EI": -0.3, "SN": 0.0, "TF": 0.0, "JP": 0.2},
            {"EI": 0.4, "SN": -0.5, "TF": 0.3, "JP": 0.0},
            {"EI": -0.2, "SN": 0.2, "TF": 0.4, "JP": 0.0},
        ],
    },
    {
        "id": 3,
        "emoji": "☀️",
        "title": "주말 아침",
        "question": "토요일 아침 10시, 햇살이 좋아요. 어디에 있고 싶어요?",
        "options": [
            "동네 카페 테라스에서 아메리카노 한 잔 + 책",
            "한강이나 공원에서 러닝 — 몸을 움직여야 주말이지",
            "늦잠 후 집에서 여유로운 브런치 — 집이 제일 편해",
            "전시회·플리마켓·팝업 — 새로운 걸 발견하러",
        ],
        "weights": [
            {"EI": 0.1, "SN": -0.4, "TF": 0.0, "JP": 0.0},
            {"EI": 0.3, "SN": 0.1, "TF": 0.0, "JP": 0.3},
            {"EI": -0.6, "SN": 0.2, "TF": 0.0, "JP": 0.0},
            {"EI": 0.3, "SN": -0.6, "TF": 0.0, "JP": 0.3},
        ],
    },
    {
        "id": 4,
        "emoji": "💰",
        "title": "이사 조건 우선순위",
        "question": "집을 구할 때, 당신의 첫 번째 조건은?",
        "options": [
            "시세 상승 가능성 — 집은 가장 큰 투자니까",
            "넓은 평수 대비 합리적 가격 — 실속이 최고",
            "역세권 + 학군 — 10년 살 수 있는 인프라",
            "동네 분위기 — 걸어다니며 기분 좋은 곳이 중요해",
        ],
        "weights": [
            {"EI": 0.0, "SN": 0.0, "TF": 0.7, "JP": 0.3},
            {"EI": 0.0, "SN": 0.2, "TF": -0.4, "JP": -0.3},
            {"EI": 0.0, "SN": 0.3, "TF": 0.2, "JP": -0.5},
            {"EI": 0.2, "SN": -0.4, "TF": -0.2, "JP": 0.0},
        ],
    },
    {
        "id": 5,
        "emoji": "🚶",
        "title": "저녁 산책",
        "question": "저녁 식사 후 30분 산책, 어떤 길을 걷고 싶어요?",
        "options": [
            "번화한 메인 거리 — 사람 구경, 쇼윈도 구경이 재밌어",
            "조용한 이면도로 — 생각 정리하며 천천히",
            "공원 산책로 — 자연 속에서 리프레시",
            "아직 안 가본 골목 탐험 — 숨은 가게 발굴이 취미",
        ],
        "weights": [
            {"EI": 0.6, "SN": -0.2, "TF": 0.0, "JP": 0.0},
            {"EI": -0.5, "SN": 0.0, "TF": 0.0, "JP": -0.2},
            {"EI": -0.1, "SN": 0.2, "TF": 0.0, "JP": -0.2},
            {"EI": 0.3, "SN": -0.5, "TF": 0.0, "JP": 0.5},
        ],
    },
    {
        "id": 6,
        "emoji": "📰",
        "title": "부동산 뉴스",
        "question": "'서울 아파트 시세 3개월째 상승' 뉴스를 봤어요. 첫 반응은?",
        "options": [
            "차트부터 확인 — 매수 타이밍인지 분석해봐야지",
            "전세 부담이 걱정... 더 합리적인 곳 알아봐야겠다",
            "우리 동네는 얼마나 올랐을까? 한번 확인해봐야지",
            "집값보다 살기 좋은 동네가 중요하지, 크게 신경 안 써",
        ],
        "weights": [
            {"EI": 0.0, "SN": 0.0, "TF": 0.7, "JP": 0.2},
            {"EI": 0.0, "SN": 0.0, "TF": -0.5, "JP": -0.3},
            {"EI": 0.0, "SN": 0.0, "TF": 0.2, "JP": -0.1},
            {"EI": 0.0, "SN": -0.3, "TF": -0.3, "JP": 0.0},
        ],
    },
    {
        "id": 7,
        "emoji": "🏪",
        "title": "동네 인프라",
        "question": "우리 동네에 딱 하나만 새로 생긴다면?",
        "options": [
            "퀄리티 좋은 동네 빵집이나 정육점",
            "분위기 있는 독립 서점이나 레코드샵",
            "24시 편의점 + 코인세탁소 — 편리함이 최고",
            "루프탑 바나 라이브 공연장 — 밤이 재밌어야 동네지",
        ],
        "weights": [
            {"EI": 0.1, "SN": 0.6, "TF": 0.0, "JP": 0.0},
            {"EI": 0.1, "SN": -0.7, "TF": 0.0, "JP": 0.0},
            {"EI": 0.0, "SN": 0.4, "TF": -0.2, "JP": -0.2},
            {"EI": 0.6, "SN": -0.4, "TF": 0.0, "JP": 0.4},
        ],
    },
    {
        "id": 8,
        "emoji": "🔮",
        "title": "미래 전망",
        "question": "5년 후 우리 동네가 이렇게 변했으면:",
        "options": [
            "지금 그대로 — 이 고요함과 안정감이 가장 큰 자산",
            "젊은 창업자와 새 가게들로 활기를 되찾은 동네",
            "교통 개선 + 학군 강화 — 살기 좋은 명문 동네로",
            "예술가·크리에이터가 모이는 문화 특구",
        ],
        "weights": [
            {"EI": -0.2, "SN": 0.0, "TF": 0.0, "JP": -0.7},
            {"EI": 0.3, "SN": -0.2, "TF": 0.0, "JP": 0.5},
            {"EI": 0.0, "SN": 0.3, "TF": 0.4, "JP": -0.3},
            {"EI": 0.2, "SN": -0.6, "TF": 0.0, "JP": 0.3},
        ],
    },
]

# ── 축별 라벨 ────────────────────────────────────────────────────────────
AXIS_LABELS = {
    "EI": {"pos": "E 외향적", "neg": "I 내향적", "pos_desc": "활기찬 상업지", "neg_desc": "조용한 주거지"},
    "SN": {"pos": "S 실용적", "neg": "N 문화적", "pos_desc": "생활 인프라 중심", "neg_desc": "트렌디한 카페거리"},
    "TF": {"pos": "T 이성적", "neg": "F 감성적", "pos_desc": "투자 가치 높은", "neg_desc": "소박하고 따뜻한"},
    "JP": {"pos": "P 변화적", "neg": "J 안정적", "pos_desc": "역동적으로 변화하는", "neg_desc": "안정적이고 검증된"},
}


# ── 스케일링 상수 ────────────────────────────────────────────────────────
# 사용자 점수(평균 ~[-0.6,+0.6])를 동네 z-score 범위(~[-2,+2])에 맞춤.
# ×3 팩터로 [-1.8,+1.8] 범위가 되어 동네 z-score 분포와 자연스럽게 매칭.
SCORE_SCALE_FACTOR = 3.0


# ── 스코어링 함수 ────────────────────────────────────────────────────────
def compute_user_scores(answers: list[int]) -> dict[str, float]:
    """
    8개 질문에 대한 답변(0~3 인덱스)을 받아 4축 선호 점수를 계산.
    동네 z-score 범위에 맞게 스케일링 적용.

    Returns: {"EI": float, "SN": float, "TF": float, "JP": float}
    """
    totals = {"EI": 0.0, "SN": 0.0, "TF": 0.0, "JP": 0.0}
    counts = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}

    for q_idx, ans_idx in enumerate(answers):
        weights = QUESTIONS[q_idx]["weights"][ans_idx]
        for axis, w in weights.items():
            if w != 0.0:
                totals[axis] += w
                counts[axis] += 1

    scores = {}
    for axis in totals:
        if counts[axis] > 0:
            raw = totals[axis] / counts[axis]
            scores[axis] = round(raw * SCORE_SCALE_FACTOR, 4)
        else:
            scores[axis] = 0.0

    return scores


def scores_to_mbti(scores: dict[str, float]) -> str:
    """4축 점수 → MBTI 4글자 문자열."""
    return (
        ("E" if scores["EI"] >= 0 else "I")
        + ("S" if scores["SN"] >= 0 else "N")
        + ("T" if scores["TF"] >= 0 else "F")
        + ("P" if scores["JP"] >= 0 else "J")
    )


def match_neighborhoods(user_scores: dict[str, float], profiles_df) -> list:
    """
    사용자 선호 점수와 118개 동네의 z-score 간 유클리드 거리 계산.
    가장 가까운 TOP 3 동네를 반환.

    Returns: [(row_dict, distance), ...] 길이 3
    """
    results = []
    for _, row in profiles_df.iterrows():
        dist = sqrt(
            (user_scores["EI"] - float(row["EI_SCORE"])) ** 2
            + (user_scores["SN"] - float(row["SN_SCORE"])) ** 2
            + (user_scores["TF"] - float(row["TF_SCORE"])) ** 2
            + (user_scores["JP"] - float(row["JP_SCORE"])) ** 2
        )
        results.append((row.to_dict(), dist))

    results.sort(key=lambda x: x[1])
    return results[:3]


def generate_user_dna_text(scores: dict[str, float], mbti: str) -> str:
    """축별 점수를 기반으로 사용자 DNA 요약 텍스트 생성 (AI 호출 없이)."""
    parts = []
    for axis in ["EI", "SN", "TF", "JP"]:
        label_info = AXIS_LABELS[axis]
        val = scores[axis]
        if val >= 0:
            direction = label_info["pos_desc"]
        else:
            direction = label_info["neg_desc"]
        parts.append(direction)

    return f"{parts[0]}, {parts[1]}, {parts[2]}, {parts[3]}"


def compute_match_pct(distance: float) -> int:
    """유클리드 거리를 0~100% 매칭률로 변환."""
    # 스케일링 후 최대 거리 ~8.0 (4축 × 최대 차이 ~4) 기준 정규화
    pct = max(0, int(100 - distance * 12.5))
    return min(100, pct)


def reset_quiz_state(session_state) -> None:
    """퀴즈 관련 session_state를 초기화하여 다시 시작."""
    for key in [
        "quiz_step", "quiz_answers", "quiz_completed",
        "quiz_user_scores", "quiz_user_mbti", "quiz_matches",
        "quiz_dna_text", "quiz_rec_texts", "quiz_ai_dna", "quiz_ai_done",
    ]:
        if key in session_state:
            del session_state[key]
