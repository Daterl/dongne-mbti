"""
동네 MBTI — 서울 동네의 성격을 찾아서
Streamlit in Snowflake App
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import altair as alt
from snowflake.snowpark.context import get_active_session
from animals import MBTI_ANIMALS, MBTI_ANIMAL_NAMES
from questions import (
    QUESTIONS, AXIS_LABELS, compute_user_scores, scores_to_mbti,
    match_neighborhoods, compute_match_pct, reset_quiz_state, generate_user_dna_text,
)
import time
import html as _html

# ── AI 모델 설정 ──────────────────────────────────────────────────────────────
# AISQL 신함수 AI_COMPLETE + Meta Llama 3.3 70B (2026-04 기준 이 리전 최신 오픈 모델)
# 'auto' 셀렉터는 본 계정/리전에서 미지원 → 최신 명시 모델로 고정, 업그레이드는 이 상수만 교체
MODEL_PRIMARY = "llama3.1-70b"        # 주 모델: Meta Llama 3.1 70B (ENZO 계정 리전 호환)
MODEL_FALLBACK = "snowflake-arctic"   # 폴백 모델: Primary 실패 시 Snowflake 네이티브


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """#RRGGBB → rgba(r,g,b,alpha) 변환 (plotly 구버전 호환)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# ── 페이지 설정 ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="동네 MBTI",
    page_icon="🏙️",
    layout="wide",
)

# ── MBTI 컬러 팔레트 ─────────────────────────────────────────────────────────
MBTI_COLORS = {
    "INTJ": "#6C3483", "INTP": "#2874A6", "ENTJ": "#1A5276", "ENTP": "#148F77",
    "INFJ": "#7D3C98", "INFP": "#C39BD3", "ENFJ": "#F39C12", "ENFP": "#E74C3C",
    "ISTJ": "#2C3E50", "ISFJ": "#5D6D7E", "ESTJ": "#283747", "ESFJ": "#D4AC0D",
    "ISTP": "#1ABC9C", "ISFP": "#A3E4D7", "ESTP": "#E67E22", "ESFP": "#F1948A",
}

MBTI_DESC = {
    "E": "외향적", "I": "내향적",
    "S": "실용적", "N": "문화적",
    "T": "이성적", "F": "감성적",
    "J": "안정적", "P": "변화적",
}

# ── Snowflake 세션 ────────────────────────────────────────────────────────────
@st.cache_resource
def get_session():
    return get_active_session()

session = get_session()

# ── 데이터 로드 함수 ──────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_mbti_result():
    return session.sql("""
        SELECT SGG, EMD, MBTI, EI_SCORE, SN_SCORE, TF_SCORE, JP_SCORE
        FROM DONGNE_MBTI.PUBLIC.DONG_MBTI_RESULT
        ORDER BY SGG, EMD
    """).to_pandas()

@st.cache_data(ttl=300)
def load_profiles():
    return session.sql("""
        SELECT SGG, EMD, MBTI, PROFILE_TEXT, CHARACTER_SUMMARY,
               EI_SCORE, SN_SCORE, TF_SCORE, JP_SCORE,
               NEIGHBORHOOD_TYPE, SENTIMENT_SCORE
        FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES
        ORDER BY SGG, EMD
    """).to_pandas()

@st.cache_data(ttl=300)
def load_price_history(sgg: str, emd: str):
    return session.sql(f"""
        SELECT YYYYMMDD, AVG(MEME_PRICE_PER_SUPPLY_PYEONG) AS AVG_PRICE
        FROM KOREAN_POPULATION__APARTMENT_MARKET_PRICE_DATA
            .HACKATHON_2025Q2.REGION_APT_RICHGO_MARKET_PRICE_M_H
        WHERE SD = '서울' AND SGG = '{sgg}' AND EMD = '{emd}'
          AND MEME_PRICE_PER_SUPPLY_PYEONG > 0
        GROUP BY YYYYMMDD
        ORDER BY YYYYMMDD
    """).to_pandas()

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── 카드 기본 ── */
.mbti-card {
    border-radius: 24px;
    padding: 32px 24px 28px;
    color: white;
    text-align: center;
    margin-bottom: 16px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.25), 0 2px 8px rgba(0,0,0,0.1);
    position: relative;
    overflow: hidden;
}
.mbti-card::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 20%, rgba(255,255,255,0.12) 0%, transparent 50%);
    pointer-events: none;
}
.mbti-animal {
    text-align: center;
    margin-bottom: 6px;
    filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3));
}
.mbti-animal img {
    transition: transform 0.3s ease;
}
.mbti-animal img:hover {
    transform: scale(1.08);
}
.mbti-animal-name {
    font-size: 14px;
    opacity: 0.85;
    margin-top: 4px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 500;
}
.mbti-type {
    font-size: 60px;
    font-weight: 900;
    letter-spacing: 8px;
    margin: 0;
    text-shadow: 0 2px 12px rgba(0,0,0,0.2);
}
.mbti-subtitle {
    font-size: 15px;
    opacity: 0.8;
    margin-top: 6px;
    font-weight: 500;
    letter-spacing: 1px;
}

/* ── 축 칩 ── */
.axis-chip {
    display: inline-block;
    border-radius: 24px;
    padding: 5px 16px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px 3px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    transition: background 0.2s ease;
}
.axis-chip:hover {
    background: rgba(255,255,255,0.28);
}

/* ── 캐릭터 요약 ── */
.character-summary {
    font-size: 16px;
    font-style: italic;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 14px;
    padding: 14px 18px;
    margin-top: 16px;
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    line-height: 1.6;
}

/* ── 섹션 타이틀 ── */
.section-title {
    font-size: 18px;
    font-weight: 700;
    color: #333;
    margin: 20px 0 10px 0;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── 베프/라이벌 카드 ── */
.bff-rival-card {
    flex: 1;
    border-radius: 16px;
    padding: 16px 14px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border: 1px solid rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    align-items: center;
}
.bff-rival-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}
.bff-rival-img {
    width: 100%;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 6px 0;
}
.bff-rival-img img {
    max-width: 72px;
    max-height: 72px;
    object-fit: contain;
    filter: drop-shadow(0 2px 6px rgba(0,0,0,0.15));
}

/* ── 순위 바 ── */
.rank-bar-container {
    margin-bottom: 10px;
}
.rank-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    margin-bottom: 4px;
    font-weight: 500;
}
.rank-bar-bg {
    background: rgba(0,0,0,0.06);
    border-radius: 8px;
    height: 10px;
    overflow: hidden;
}
.rank-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.6s ease;
    box-shadow: 0 0 8px rgba(0,0,0,0.1);
}

/* ── 같은 MBTI 동네 ── */
.same-mbti-box {
    background: linear-gradient(135deg, rgba(0,0,0,0.03), rgba(0,0,0,0.06));
    border-radius: 14px;
    padding: 14px 18px;
    margin-top: 12px;
    border: 1px solid rgba(0,0,0,0.06);
}

/* ── 케미 카드 ── */
.chem-card {
    border-radius: 16px;
    padding: 18px 20px;
    margin-top: 10px;
    text-align: center;
    font-size: 16px;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

/* ── 캐릭터 대화 ── */
.char-dialogue {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    gap: 16px;
    margin-top: 20px;
    padding: 20px 0;
}
.char-dialogue-unit {
    text-align: center;
    flex: 0 0 auto;
}
.char-bubble {
    background: rgba(0,0,0,0.05);
    border-radius: 18px;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 14px;
    position: relative;
    display: inline-block;
    max-width: 170px;
    border: 1px solid rgba(0,0,0,0.06);
    line-height: 1.5;
}
.char-bubble::after {
    content: '';
    position: absolute;
    bottom: -7px;
    left: 50%;
    transform: translateX(-50%);
    width: 0; height: 0;
    border-left: 7px solid transparent;
    border-right: 7px solid transparent;
    border-top: 7px solid rgba(0,0,0,0.05);
}
.char-dialogue-label {
    font-size: 12px;
    opacity: 0.6;
    margin-top: 6px;
    line-height: 1.4;
}

/* ── 뱃지 ── */
.badge {
    display: inline-block;
    border-radius: 24px;
    padding: 5px 16px;
    font-size: 13px;
    font-weight: 600;
}
.badge-type {
    background: linear-gradient(135deg, #f0f2f6, #e8eaed);
    color: #444;
}

/* ── 유틸리티 ── */
.vs-icon {
    font-size: 32px;
    align-self: center;
    margin: 0 10px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

/* ── 탭 헤더 ── */
.tab-header {
    margin-bottom: 16px;
}
.tab-header h3 {
    margin: 0 0 4px 0;
    font-size: 22px;
    font-weight: 700;
}
.tab-header p {
    font-size: 14px;
    opacity: 0.55;
    margin: 0;
    line-height: 1.5;
}

/* ── 채팅 메시지 ── */
.chat-msg {
    padding: 12px 16px;
    border-radius: 16px;
    margin-bottom: 10px;
    font-size: 15px;
    line-height: 1.6;
}
.chat-msg-user {
    background: linear-gradient(135deg, #2563EB, #3B82F6);
    color: white;
    margin-left: 20%;
    border-bottom-right-radius: 4px;
}
.chat-msg-ai {
    background: rgba(0,0,0,0.04);
    border: 1px solid rgba(0,0,0,0.06);
    margin-right: 20%;
    border-bottom-left-radius: 4px;
}

/* ── 추천 질문 그리드 ── */
.suggestion-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin: 12px 0;
}
.suggestion-card {
    background: rgba(0,0,0,0.03);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 12px;
    padding: 12px 14px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
    line-height: 1.4;
}
.suggestion-card:hover {
    background: rgba(37,99,235,0.08);
    border-color: rgba(37,99,235,0.2);
    transform: translateY(-1px);
}

/* ── 빈 상태 ── */
.empty-state {
    text-align: center;
    padding: 40px 20px;
    opacity: 0.5;
}
.empty-state-icon {
    font-size: 48px;
    margin-bottom: 12px;
}
.empty-state-text {
    font-size: 15px;
    line-height: 1.5;
}

/* ── 인포 카드 ── */
.info-card {
    background: linear-gradient(135deg, rgba(37,99,235,0.05), rgba(59,130,246,0.08));
    border: 1px solid rgba(37,99,235,0.12);
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 16px;
    font-size: 14px;
    line-height: 1.6;
}

/* ── 메트릭 강조 ── */
.metric-highlight {
    background: linear-gradient(135deg, rgba(0,0,0,0.02), rgba(0,0,0,0.04));
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    border: 1px solid rgba(0,0,0,0.05);
}

/* ── 탭 간 연결 CTA ── */
.next-tab-cta {
    background: linear-gradient(135deg, rgba(37,99,235,0.06), rgba(59,130,246,0.10));
    border: 1px solid rgba(37,99,235,0.15);
    border-radius: 14px;
    padding: 16px 20px;
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    line-height: 1.5;
}
.next-tab-cta-icon {
    font-size: 24px;
    flex-shrink: 0;
}
.next-tab-cta-text b {
    font-size: 15px;
}
.next-tab-cta-text span {
    opacity: 0.6;
    font-size: 13px;
}

/* ── 퀴즈 ── */
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.15); opacity: 0.7; }
}
.quiz-wrap {
    max-width: 640px;
    margin: 0 auto;
    animation: fadeSlideIn 0.35s ease;
}
.quiz-progress {
    height: 6px;
    border-radius: 3px;
    background: rgba(0,0,0,0.06);
    margin-bottom: 24px;
    overflow: hidden;
}
.quiz-progress-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, #2563EB, #60A5FA);
    transition: width 0.6s ease;
}
.quiz-emoji { font-size: 48px; text-align: center; margin-bottom: 8px; }
.quiz-title { font-size: 14px; text-align: center; opacity: 0.6; font-weight: 600; letter-spacing: 1px; margin-bottom: 8px; }
.quiz-question { font-size: 20px; font-weight: 700; text-align: center; margin-bottom: 24px; line-height: 1.5; }
.quiz-step-label { text-align: center; font-size: 13px; opacity: 0.55; margin-bottom: 16px; }
.pulse-emoji { font-size: 64px; animation: pulse 1.5s ease-in-out infinite; text-align: center; margin: 40px 0 16px; }
.result-dna-card {
    border-radius: 24px; padding: 32px 24px; color: white; text-align: center;
    margin-bottom: 20px; box-shadow: 0 12px 40px rgba(0,0,0,0.25);
    position: relative; overflow: hidden;
}
.result-dna-card::before {
    content: ''; position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 20%, rgba(255,255,255,0.12) 0%, transparent 50%);
    pointer-events: none;
}
.match-card {
    border-radius: 16px; padding: 20px; margin-bottom: 12px;
    border: 1px solid rgba(0,0,0,0.08); box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    animation: fadeSlideIn 0.4s ease;
}
.match-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
.match-card img { max-width: 56px; max-height: 56px; object-fit: contain; }
.match-rank { font-size: 13px; font-weight: 700; opacity: 0.5; letter-spacing: 1px; margin-bottom: 8px; }
.match-name { font-size: 20px; font-weight: 700; margin-bottom: 4px; }
.match-pct { font-size: 15px; font-weight: 600; color: #2563EB; margin-bottom: 8px; }
.axis-match-row {
    display: flex; align-items: center; gap: 8px; margin: 4px 0; font-size: 12px;
}
.axis-match-label {
    width: 80px; font-weight: 600; opacity: 0.7; flex-shrink: 0;
}
.axis-match-track {
    flex: 1; height: 8px; border-radius: 4px;
    background: rgba(0,0,0,0.06); overflow: hidden; min-width: 0;
}
.axis-match-fill {
    height: 100%; border-radius: 4px;
    transition: width 0.6s ease;
    box-shadow: 0 0 6px rgba(0,0,0,0.08);
}
.axis-match-val {
    width: 36px; text-align: right; font-weight: 700; flex-shrink: 0;
}
.quiz-match-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 24px; font-size: 13px; font-weight: 600;
    background: linear-gradient(135deg, rgba(37,99,235,0.08), rgba(59,130,246,0.15));
    border: 1px solid rgba(37,99,235,0.2); color: #2563EB; margin-bottom: 12px;
}
.result-banner {
    border-radius: 14px; padding: 10px 18px; margin-bottom: 12px;
    display: flex; align-items: center; gap: 10px; font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ── 헤더 ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:4px;">
    <h1 style="margin-bottom:0;font-size:36px;">🏙️ 동네 MBTI</h1>
    <p style="font-size:15px;opacity:0.6;margin-top:2px;letter-spacing:0.5px;">
        서울 동네의 성격을 데이터로 읽다 — 서초 · 영등포 · 중구 118개 동
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 성향 테스트 퀴즈 (Full-Page Gate)
# ═══════════════════════════════════════════════════════════════════════════════

for _qk, _qv in [("quiz_step", 0), ("quiz_answers", []), ("quiz_completed", False)]:
    if _qk not in st.session_state:
        st.session_state[_qk] = _qv


def _quiz_ai(prompt: str) -> str:
    """AI_COMPLETE 2-tier fallback: llama3.3-70b → snowflake-arctic → empty."""
    p = prompt.replace("'", "''")
    try:
        return session.sql(
            f"SELECT AI_COMPLETE('{MODEL_PRIMARY}', '{p}') AS R"
        ).collect()[0]["R"]
    except Exception:
        try:
            return session.sql(
                f"SELECT AI_COMPLETE('{MODEL_FALLBACK}', '{p}') AS R"
            ).collect()[0]["R"]
        except Exception:
            return ""


def _quiz_cortex_search(query: str) -> str:
    """Cortex Search 동네 프로필 보강. 실패 시 빈 문자열."""
    try:
        import _snowflake
        import json
        resp = _snowflake.send_snow_api_request(
            "POST",
            "/api/v2/databases/DONGNE_MBTI/schemas/PUBLIC/cortex-search-services/DONGNE_SEARCH:query",
            {}, {},
            {"query": query, "columns": ["PROFILE_TEXT"], "limit": 3},
            None, 30000,
        )
        if resp.get("status") == 200:
            data = json.loads(resp.get("content", "{}"))
            return "\n".join(r.get("PROFILE_TEXT", "") for r in data.get("results", []))
    except Exception:
        pass
    return ""


if not st.session_state.quiz_completed:
    step = st.session_state.quiz_step

    # ── Step 0: 인트로 ────────────────────────────────────────────────────
    if step == 0:
        st.markdown("""
        <div class="quiz-wrap" style="text-align:center;padding:40px 0 20px;">
            <div style="font-size:64px;margin-bottom:16px;">🧭</div>
            <h1 style="font-size:28px;font-weight:800;margin:0 0 8px;">나의 동네 DNA 테스트</h1>
            <p style="font-size:15px;opacity:0.6;margin:0 0 32px;line-height:1.6;">
                8개의 질문으로 118개 동네 중<br>당신에게 딱 맞는 곳을 찾아드려요
            </p>
        </div>
        """, unsafe_allow_html=True)

        prev_cols = st.columns(4)
        for i, mtype in enumerate(["ENFP", "ISTJ", "INFJ", "ESTP"]):
            with prev_cols[i]:
                st.markdown(f"""
                <div style="text-align:center;">
                    <div style="max-width:80px;margin:0 auto;">{MBTI_ANIMALS.get(mtype, "")}</div>
                    <div style="font-size:11px;opacity:0.5;margin-top:4px;">{MBTI_ANIMAL_NAMES.get(mtype, "")}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            if st.button("🧭 시작하기", use_container_width=True, type="primary"):
                st.session_state.quiz_step = 1
                st.experimental_rerun()
        with c2:
            if st.button("바로 둘러보기 →", use_container_width=True):
                st.session_state.quiz_completed = True
                st.experimental_rerun()

    # ── Step 1-8: 질문 ────────────────────────────────────────────────────
    elif 1 <= step <= 8:
        q = QUESTIONS[step - 1]
        pct = int((step - 1) / 8 * 100)

        st.markdown(f"""
        <div class="quiz-wrap">
            <div class="quiz-progress"><div class="quiz-progress-fill" style="width:{pct}%;"></div></div>
            <div class="quiz-step-label">질문 {step} / 8</div>
            <div class="quiz-emoji">{q["emoji"]}</div>
            <div class="quiz-title">{q["title"]}</div>
            <div class="quiz-question">{q["question"]}</div>
        </div>
        """, unsafe_allow_html=True)

        for oi, ot in enumerate(q["options"]):
            if st.button(ot, key=f"q{step}_o{oi}", use_container_width=True):
                st.session_state.quiz_answers.append(oi)
                st.session_state.quiz_step = step + 1
                st.experimental_rerun()

        if step > 1:
            if st.button("← 이전 질문", key=f"back_{step}"):
                st.session_state.quiz_answers.pop()
                st.session_state.quiz_step = step - 1
                st.experimental_rerun()

    # ── Step 9: 분석 중 (스코어링 + AI 호출을 애니메이션 중 수행) ──────────
    elif step == 9:
        # 애니메이션 먼저 렌더 (AI 호출 중 사용자에게 보임)
        st.markdown("""
        <div class="quiz-wrap" style="text-align:center;padding:60px 0;">
            <div class="pulse-emoji">🔍</div>
            <p style="font-size:18px;font-weight:600;margin:16px 0 8px;">
                당신의 동네 DNA를 분석하고 있어요...
            </p>
            <p style="font-size:14px;opacity:0.55;">8개 답변 × 4축 성향을 118개 동네와 매칭 중</p>
        </div>
        """, unsafe_allow_html=True)

        # 스코어링
        scores = compute_user_scores(st.session_state.quiz_answers)
        mbti = scores_to_mbti(scores)
        profiles_df = load_profiles()
        if profiles_df.empty:
            st.error("동네 프로필 데이터를 불러올 수 없습니다.")
            if st.button("처음으로"):
                reset_quiz_state(st.session_state)
                st.experimental_rerun()
            st.stop()
        matches = match_neighborhoods(scores, profiles_df)
        dna_text = generate_user_dna_text(scores, mbti)

        st.session_state.quiz_user_scores = scores
        st.session_state.quiz_user_mbti = mbti
        st.session_state.quiz_matches = matches
        st.session_state.quiz_dna_text = dna_text

        # AI 호출 (애니메이션이 보이는 동안 실행)
        axis_lines = []
        for ax, name in [("EI", "외향-내향"), ("SN", "실용-문화"),
                         ("TF", "이성-감성"), ("JP", "변화-안정")]:
            v = scores[ax]
            desc = AXIS_LABELS[ax]["pos_desc"] if v >= 0 else AXIS_LABELS[ax]["neg_desc"]
            axis_lines.append(f"- {name}: {v:+.1f} ({desc})")

        dna_prompt = (
            "당신은 서울 동네 라이프스타일 분석 전문가입니다. "
            "한국어 ~요체를 사용해주세요.\n\n"
            f"사용자의 동네 MBTI: {mbti}\n"
            + "\n".join(axis_lines)
            + "\n\n이 사람의 동네 선호 성향을 3-4문장으로 "
            "자연스럽고 따뜻하게 분석해주세요."
        )
        st.session_state.quiz_ai_dna = _quiz_ai(dna_prompt)

        rec_texts = []
        for idx, (row_dict, dist) in enumerate(matches):
            sgg, emd = row_dict["SGG"], row_dict["EMD"]
            dong_mbti = row_dict["MBTI"]
            match_pct_val = compute_match_pct(dist)
            profile = str(row_dict.get("PROFILE_TEXT", ""))[:400]

            extra = ""
            if idx == 0:
                ctx = _quiz_cortex_search(
                    f"{sgg} {emd} 동네 라이프스타일 특성"
                )
                if ctx:
                    extra = f"\n추가 정보: {ctx[:300]}"

            rec_prompt = (
                "당신은 서울 동네 추천 전문가입니다. "
                "한국어 ~요체를 사용해주세요.\n\n"
                f"사용자 MBTI: {mbti}, "
                f"추천 동네: {sgg} {emd} "
                f"(MBTI: {dong_mbti}, 매칭률: {match_pct_val}%)\n"
                f"동네 프로필: {profile}{extra}\n\n"
                "이 동네가 사용자에게 잘 맞는 이유를 "
                "2-3문장으로 설명해주세요. "
                "동네의 구체적 특성을 언급하세요."
            )
            rec_texts.append(_quiz_ai(rec_prompt))

        st.session_state.quiz_rec_texts = rec_texts
        st.session_state.quiz_ai_done = True
        st.session_state.quiz_step = 10
        st.experimental_rerun()

    # ── Step 10: 결과 (모든 데이터가 session_state에 준비됨) ──────────────
    elif step == 10:
        scores = st.session_state.quiz_user_scores
        mbti = st.session_state.quiz_user_mbti
        matches = st.session_state.quiz_matches
        color = MBTI_COLORS.get(mbti, "#555")
        animal_svg = MBTI_ANIMALS.get(mbti, "")
        animal_name = MBTI_ANIMAL_NAMES.get(mbti, "")

        # Phase A: 나의 동네 DNA 카드
        ei = "E 외향적" if scores["EI"] >= 0 else "I 내향적"
        sn = "S 실용적" if scores["SN"] >= 0 else "N 문화적"
        tf = "T 이성적" if scores["TF"] >= 0 else "F 감성적"
        jp = "P 변화적" if scores["JP"] >= 0 else "J 안정적"

        st.markdown(f"""
        <div style="max-width:480px;margin:0 auto;">
            <div class="result-dna-card" style="background:linear-gradient(145deg, {color}, {color}bb, {color}dd);">
                <div class="mbti-animal">{animal_svg}</div>
                <p class="mbti-type">{mbti}</p>
                <p class="mbti-animal-name">{animal_name}</p>
                <p style="font-size:14px;opacity:0.7;margin-top:12px;">나의 동네 DNA</p>
                <div style="margin-top:10px;">
                    <span class="axis-chip">{ei}</span>
                    <span class="axis-chip">{sn}</span>
                    <span class="axis-chip">{tf}</span>
                    <span class="axis-chip">{jp}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # AI 분석 텍스트 표시 (HTML escape로 XSS 방지)
        _raw_dna = st.session_state.get("quiz_ai_dna") or ""
        ai_dna = _html.escape(_raw_dna.strip() if _raw_dna.strip() else st.session_state.quiz_dna_text)
        st.markdown(f"""
        <div style="max-width:480px;margin:0 auto 24px;">
            <div class="info-card">
                <b>🧬 AI 성향 분석</b><br><br>
                {ai_dna}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Phase B: TOP 3 매칭
        _top1_name = f"{matches[0][0]['SGG']} {matches[0][0]['EMD']}" if matches else ""
        _top1_pct = compute_match_pct(matches[0][1]) if matches else 0
        st.markdown(f"""
        <div style="text-align:center;margin:32px 0 16px;">
            <h3 style="margin:0;">🏘️ 당신에게 딱 맞는 동네 TOP 3</h3>
            <p style="font-size:15px;opacity:0.7;margin-top:6px;">
                <b>{mbti}</b> 성향의 당신, <b>{_top1_name}</b>과 <b style="color:#2563EB;">{_top1_pct}%</b> 매칭!
            </p>
        </div>
        """, unsafe_allow_html=True)

        rec_texts = st.session_state.get("quiz_rec_texts", ["", "", ""])
        _AXIS_KR = {"EI": "활동성", "SN": "라이프스타일", "TF": "경제관", "JP": "안정성"}

        # 1위 → 2위 → 3위 순서
        for rank_idx in range(len(matches)):
            row_dict, dist = matches[rank_idx]
            rank = rank_idx + 1
            dong_mbti = row_dict["MBTI"]
            dong_animal = MBTI_ANIMALS.get(dong_mbti, "")
            dong_animal_name = MBTI_ANIMAL_NAMES.get(dong_mbti, "")
            pct = compute_match_pct(dist)
            rec = rec_texts[rank_idx] if rank_idx < len(rec_texts) else ""
            medal = ["🥇", "🥈", "🥉"][rank_idx]

            # 축별 매칭률 바 HTML
            axis_html = ""
            for ax in ["EI", "SN", "TF", "JP"]:
                uv = scores[ax]
                _raw_dv = row_dict.get(f"{ax}_SCORE", 0)
                dv = float(_raw_dv) if _raw_dv == _raw_dv else 0.0  # NaN guard
                diff = abs(uv - dv)
                ax_pct = max(0, min(100, int(100 * __import__('math').exp(-diff * 0.7))))
                if ax_pct >= 80:
                    bar_color = "linear-gradient(90deg, #2563EB, #60A5FA)"
                    val_color = "#2563EB"
                elif ax_pct >= 60:
                    bar_color = "linear-gradient(90deg, #F59E0B, #FBBF24)"
                    val_color = "#D97706"
                else:
                    bar_color = "linear-gradient(90deg, #9CA3AF, #D1D5DB)"
                    val_color = "#6B7280"
                axis_html += (
                    '<div class="axis-match-row">'
                    f'<span class="axis-match-label">{_AXIS_KR[ax]}</span>'
                    f'<div class="axis-match-track">'
                    f'<div class="axis-match-fill" style="width:{ax_pct}%;'
                    f'background:{bar_color};"></div></div>'
                    f'<span class="axis-match-val" style="color:{val_color};">'
                    f'{ax_pct}%</span>'
                    '</div>'
                )

            rec_html = ""
            if rec:
                rec_safe = _html.escape(rec)
                rec_html = (
                    '<div style="margin-top:12px;padding:10px 14px;'
                    'background:rgba(37,99,235,0.04);border-radius:10px;'
                    f'font-size:14px;line-height:1.6;">💡 {rec_safe}</div>'
                )

            st.markdown(f"""
            <div class="match-card" style="max-width:640px;margin:0 auto 16px;">
                <div class="match-rank">{medal} {rank}위 매칭</div>
                <div style="display:flex;gap:16px;align-items:center;">
                    <div style="width:64px;text-align:center;flex-shrink:0;">
                        {dong_animal}
                    </div>
                    <div style="flex:1;">
                        <div class="match-name">{row_dict["SGG"]} {row_dict["EMD"]}</div>
                        <div style="font-size:13px;opacity:0.6;">
                            {dong_mbti} · {dong_animal_name}
                        </div>
                        <div class="match-pct" style="{'font-size:20px;' if rank == 1 else ''}">매칭률 {pct}%</div>
                    </div>
                </div>
                <div style="margin-top:14px;padding-top:12px;border-top:1px solid rgba(0,0,0,0.06);">
                    {axis_html}
                </div>
                {rec_html}
            </div>
            """, unsafe_allow_html=True)

        # CTA 버튼
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        c_go, c_retry = st.columns([2, 1])
        with c_go:
            if st.button("🏙️ 1위 동네 둘러보기", use_container_width=True, type="primary"):
                st.session_state.quiz_completed = True
                if matches:
                    st.session_state["_quiz_nav_target"] = {
                        "sgg": matches[0][0]["SGG"],
                        "emd": matches[0][0]["EMD"],
                    }
                st.experimental_rerun()
        with c_retry:
            if st.button("🔄 다시 하기", use_container_width=True):
                reset_quiz_state(st.session_state)
                st.experimental_rerun()

    st.stop()

# ── 결과 배너 (퀴즈 완료 후, 탭 위에 표시) ──────────────────────────────────
if st.session_state.get("quiz_user_mbti"):
    _bm = st.session_state.quiz_user_mbti
    _bc = MBTI_COLORS.get(_bm, "#555")
    _ba = MBTI_ANIMAL_NAMES.get(_bm, "")
    _binfo = ""
    _matches = st.session_state.get("quiz_matches")
    if _matches and len(_matches) > 0:
        _t1 = _matches[0][0]
        _t1p = compute_match_pct(_matches[0][1])
        _binfo = f" · 🏘️ TOP 1: {_t1['SGG']} {_t1['EMD']} ({_t1p}%)"
    _bcol1, _bcol2 = st.columns([5, 1])
    with _bcol1:
        st.markdown(f"""
        <div class="result-banner" style="background:linear-gradient(135deg, {_bc}15, {_bc}25);
             border:1px solid {_bc}30;">
            <span style="font-size:18px;">🧬</span>
            <span>나의 동네 DNA: <b style="color:{_bc};">{_bm}</b> {_ba}{_binfo}</span>
        </div>
        """, unsafe_allow_html=True)
    with _bcol2:
        if st.button("🔄 다시 테스트", key="banner_retry"):
            reset_quiz_state(st.session_state)
            st.experimental_rerun()

# ── 탭 ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🏠 동네 카드", "💬 동네 찾기", "📊 시세 전망", "🔬 데이터 탐색"])

# ════════════════════════════════════════════════════════════════════════════
# 탭 1: 동네 MBTI 카드
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    profiles_df = load_profiles()

    # 퀴즈 네비게이션 핸들러 (CTA 또는 퀵네비 버튼에서 설정)
    _quiz_nav = st.session_state.pop("_quiz_nav_target", None)
    if _quiz_nav:
        st.session_state["t1_gu"] = _quiz_nav["sgg"]
        st.session_state["t1_emd"] = _quiz_nav["emd"]

    # 퀴즈 매칭 퀵 네비게이션
    _qm = st.session_state.get("quiz_matches")
    if _qm and st.session_state.get("quiz_completed"):
        _qn_cols = st.columns(len(_qm))
        for _qi, (_qr, _qd) in enumerate(_qm):
            with _qn_cols[_qi]:
                _qmedal = ["🥇", "🥈", "🥉"][_qi]
                _qpct = compute_match_pct(_qd)
                if st.button(
                    f"{_qmedal} {_qr['EMD']} ({_qpct}%)",
                    key=f"qnav_{_qi}",
                    use_container_width=True,
                ):
                    st.session_state["_quiz_nav_target"] = {
                        "sgg": _qr["SGG"], "emd": _qr["EMD"],
                    }
                    st.experimental_rerun()

    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        gu_list = sorted(profiles_df["SGG"].unique())
        selected_gu = st.selectbox("구 선택", gu_list, key="t1_gu")
    with col_sel2:
        dong_list = sorted(profiles_df[profiles_df["SGG"] == selected_gu]["EMD"].unique())
        # 네비게이션된 동이 현재 구에 없으면 키 제거 (Streamlit 위젯 오류 방지)
        if "t1_emd" in st.session_state and st.session_state["t1_emd"] not in dong_list:
            del st.session_state["t1_emd"]
        selected_dong = st.selectbox("동 선택", dong_list, key="t1_emd")

    row = profiles_df[
        (profiles_df["SGG"] == selected_gu) & (profiles_df["EMD"] == selected_dong)
    ]

    if row.empty:
        st.warning("해당 동의 데이터가 없습니다.")
        st.stop()

    row = row.iloc[0]
    mbti = row["MBTI"]
    color = MBTI_COLORS.get(mbti, "#555")

    # 퀴즈 매칭 뱃지 (현재 동네가 TOP 3에 포함될 때)
    if _qm:
        for _mi, (_mr, _md) in enumerate(_qm):
            if _mr["SGG"] == selected_gu and _mr["EMD"] == selected_dong:
                _mm = ["🥇", "🥈", "🥉"][_mi]
                _mp = compute_match_pct(_md)
                st.markdown(
                    f'<div class="quiz-match-badge">{_mm} 당신과 {_mp}% 매칭된 동네</div>',
                    unsafe_allow_html=True,
                )
                break

    # 4축 라벨
    ei = "E 외향적" if row["EI_SCORE"] >= 0 else "I 내향적"
    sn = "S 실용적" if row["SN_SCORE"] >= 0 else "N 문화적"
    tf = "T 이성적" if row["TF_SCORE"] >= 0 else "F 감성적"
    jp = "P 변화적" if row["JP_SCORE"] >= 0 else "J 안정적"

    col_card, col_chart = st.columns([1, 1])

    # ── MBTI 카드 ──
    with col_card:
        animal_svg = MBTI_ANIMALS.get(mbti, "")
        animal_name = MBTI_ANIMAL_NAMES.get(mbti, "")
        st.markdown(f"""
        <div class="mbti-card" style="background: linear-gradient(145deg, {color}, {color}bb, {color}dd);">
            <div class="mbti-animal">{animal_svg}</div>
            <p class="mbti-type">{mbti}</p>
            <p class="mbti-animal-name">{animal_name}</p>
            <p class="mbti-subtitle">{selected_gu} {selected_dong}</p>
            <div style="margin-top:10px;">
                <span class="axis-chip">{ei}</span>
                <span class="axis-chip">{sn}</span>
                <span class="axis-chip">{tf}</span>
                <span class="axis-chip">{jp}</span>
            </div>
            <div class="character-summary">"{row['CHARACTER_SUMMARY']}"</div>
        </div>
        """, unsafe_allow_html=True)

        # AI_CLASSIFY 결과: 동네 유형 뱃지
        neighborhood_type = row.get("NEIGHBORHOOD_TYPE")
        if neighborhood_type and str(neighborhood_type) not in ("None", "nan", ""):
            st.markdown(
                f'<span class="badge badge-type">🏷️ {neighborhood_type}</span>',
                unsafe_allow_html=True,
            )

        # AI_SENTIMENT 결과: 감성 점수
        sentiment = row.get("SENTIMENT_SCORE")
        if sentiment is not None and str(sentiment) not in ("None", "nan", ""):
            try:
                s_val = float(sentiment)
                s_label = "긍정적" if s_val > 0.1 else ("부정적" if s_val < -0.1 else "중립적")
                s_color = "#27ae60" if s_val > 0.1 else ("#e74c3c" if s_val < -0.1 else "#888")
                st.markdown(
                    f'<span style="color:{s_color};font-size:13px;font-weight:600;">'
                    f'💬 AI 감성 분석: {s_label} ({s_val:+.2f})</span>',
                    unsafe_allow_html=True,
                )
            except (ValueError, TypeError):
                pass

        # ── 베프 동네 / 라이벌 동네 ──
        all_df = load_mbti_result()
        others = all_df[~((all_df["SGG"] == selected_gu) & (all_df["EMD"] == selected_dong))].copy()
        _axes = ["EI_SCORE", "SN_SCORE", "TF_SCORE", "JP_SCORE"]
        others["_dist"] = others.apply(lambda r: sum(abs(row[a] - r[a]) for a in _axes), axis=1)
        best = others.loc[others["_dist"].idxmin()]
        rival = others.loc[others["_dist"].idxmax()]
        best_animal = MBTI_ANIMAL_NAMES.get(best["MBTI"], "")
        rival_animal = MBTI_ANIMAL_NAMES.get(rival["MBTI"], "")

        best_color = MBTI_COLORS.get(best["MBTI"], "#27ae60")
        rival_color = MBTI_COLORS.get(rival["MBTI"], "#e74c3c")
        best_img = MBTI_ANIMALS.get(best["MBTI"], "")
        rival_img = MBTI_ANIMALS.get(rival["MBTI"], "")
        st.markdown(f"""
        <div style="display:flex;gap:10px;margin:12px 0;">
            <div class="bff-rival-card" style="background:linear-gradient(135deg, rgba(39,174,96,0.08), rgba(39,174,96,0.15));">
                <div style="font-size:12px;opacity:0.6;font-weight:600;letter-spacing:1px;margin-bottom:6px;">🤝 베프 동네</div>
                <div class="bff-rival-img">{best_img}</div>
                <div style="font-size:17px;font-weight:700;margin:4px 0;">{best["SGG"]} {best["EMD"]}</div>
                <div style="font-size:13px;opacity:0.7;font-weight:500;">{best["MBTI"]} {best_animal}</div>
            </div>
            <div class="bff-rival-card" style="background:linear-gradient(135deg, rgba(231,76,60,0.08), rgba(231,76,60,0.15));">
                <div style="font-size:12px;opacity:0.6;font-weight:600;letter-spacing:1px;margin-bottom:6px;">⚡ 라이벌 동네</div>
                <div class="bff-rival-img">{rival_img}</div>
                <div style="font-size:17px;font-weight:700;margin:4px 0;">{rival["SGG"]} {rival["EMD"]}</div>
                <div style="font-size:13px;opacity:0.7;font-weight:500;">{rival["MBTI"]} {rival_animal}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-title">동네 성격 분석</p>', unsafe_allow_html=True)
        st.markdown(row["PROFILE_TEXT"])

    # ── 레이더 차트 ──
    with col_chart:
        scores = [row["EI_SCORE"], row["SN_SCORE"], row["TF_SCORE"], row["JP_SCORE"]]
        categories = ["E/I 활동성", "S/N 라이프", "T/F 경제력", "J/P 안정성"]
        # 0~1 정규화 (최대 절댓값 3으로 클리핑)
        normalized = [max(0, min(1, (s + 3) / 6)) for s in scores]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=normalized + [normalized[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor=hex_to_rgba(color, 0.33),
            line=dict(color=color, width=2),
            name=mbti,
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=False, range=[0, 1]),
                angularaxis=dict(tickfont=dict(size=13)),
            ),
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})

        # 4축 수치 메트릭
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("E/I", f"{row['EI_SCORE']:+.2f}", help="양수=외향(E), 음수=내향(I)")
        c2.metric("S/N", f"{row['SN_SCORE']:+.2f}", help="양수=실용(S), 음수=문화(N)")
        c3.metric("T/F", f"{row['TF_SCORE']:+.2f}", help="양수=이성/부유(T), 음수=감성/서민(F)")
        c4.metric("J/P", f"{row['JP_SCORE']:+.2f}", help="양수=변화(P), 음수=안정(J)")

        # ── 축별 순위 ──
        rank_df = load_mbti_result()
        total_dongs = len(rank_df)
        rank_labels = {"EI_SCORE": "E/I 활동성", "SN_SCORE": "S/N 라이프", "TF_SCORE": "T/F 경제력", "JP_SCORE": "J/P 안정성"}
        rank_html = ""
        for axis, label in rank_labels.items():
            rank = int((rank_df[axis] > row[axis]).sum()) + 1
            pct = int(rank / total_dongs * 100)
            fill_pct = 100 - pct
            bar_gradient = f"linear-gradient(90deg, {color}, {color}aa)" if pct <= 50 else "linear-gradient(90deg, #aaa, #888)"
            rank_emoji = "🥇" if rank <= 3 else ("🥈" if rank <= 10 else "")
            rank_html += f"""
            <div class="rank-bar-container">
                <div class="rank-bar-label">
                    <span>{label}</span><span style="opacity:0.6;">{rank_emoji} {rank}위 / {total_dongs}개 동</span>
                </div>
                <div class="rank-bar-bg">
                    <div class="rank-bar-fill" style="width:{fill_pct}%;background:{bar_gradient};"></div>
                </div>
            </div>"""
        st.markdown(f'<div style="margin-top:14px;">{rank_html}</div>', unsafe_allow_html=True)

        # ── 같은 MBTI 동네 ──
        same_mbti = rank_df[rank_df["MBTI"] == mbti]
        same_others = same_mbti[~((same_mbti["SGG"] == selected_gu) & (same_mbti["EMD"] == selected_dong))]
        same_list = [f"{r['SGG']} {r['EMD']}" for _, r in same_others.iterrows()]
        if same_list:
            names = " · ".join(same_list[:8])
            extra = f" 외 {len(same_list) - 8}곳" if len(same_list) > 8 else ""
            st.markdown(
                f'<div class="same-mbti-box">'
                f'<div style="font-size:13px;opacity:0.6;font-weight:600;margin-bottom:6px;">🏘️ 같은 {mbti} 동네 ({len(same_mbti)}곳)</div>'
                f'<div style="font-size:14px;line-height:1.6;">{names}{extra}</div></div>',
                unsafe_allow_html=True,
            )

    # ── 동네 비교 ──
    st.divider()
    st.markdown("""
    <div style="margin-bottom:8px;">
        <span style="font-size:22px;font-weight:700;">🔍 다른 동네와 비교</span>
        <span style="font-size:13px;opacity:0.5;margin-left:8px;">MBTI 궁합을 확인해 보세요</span>
    </div>
    """, unsafe_allow_html=True)

    all_df = load_mbti_result()
    compare_options = [
        f"{r['SGG']} {r['EMD']} ({r['MBTI']})"
        for _, r in all_df[~((all_df["SGG"] == selected_gu) & (all_df["EMD"] == selected_dong))].iterrows()
    ]
    selected_compare = st.selectbox("비교할 동네", compare_options)

    if selected_compare:
        parts = selected_compare.split()
        c_gu, c_dong = parts[0], parts[1]
        c_row = all_df[(all_df["SGG"] == c_gu) & (all_df["EMD"] == c_dong)].iloc[0]
        c_color = MBTI_COLORS.get(c_row["MBTI"], "#888")

        axes = ["EI_SCORE", "SN_SCORE", "TF_SCORE", "JP_SCORE"]
        labels = ["E/I 활동성", "S/N 라이프", "T/F 경제력", "J/P 안정성"]

        fig2 = go.Figure()
        # 현재 동
        fig2.add_trace(go.Scatterpolar(
            r=[max(0, min(1, (row[a] + 3) / 6)) for a in axes] + [max(0, min(1, (row[axes[0]] + 3) / 6))],
            theta=labels + [labels[0]],
            fill="toself",
            fillcolor=hex_to_rgba(color, 0.27),
            line=dict(color=color, width=2),
            name=f"{selected_dong} ({mbti})",
        ))
        # 비교 동
        fig2.add_trace(go.Scatterpolar(
            r=[max(0, min(1, (c_row[a] + 3) / 6)) for a in axes] + [max(0, min(1, (c_row[axes[0]] + 3) / 6))],
            theta=labels + [labels[0]],
            fill="toself",
            fillcolor=hex_to_rgba(c_color, 0.27),
            line=dict(color=c_color, width=2, dash="dash"),
            name=f"{c_dong} ({c_row['MBTI']})",
        ))
        fig2.update_layout(
            polar=dict(radialaxis=dict(visible=False, range=[0, 1])),
            margin=dict(t=30, b=20, l=20, r=20),
            height=340,
            legend=dict(orientation="h", yanchor="bottom", y=1.05),
        )
        st.plotly_chart(fig2, use_container_width=True, config={"staticPlot": True})

        # 궁합 점수 (축별 거리 기반)
        distance = sum(abs(row[a] - c_row[a]) for a in axes)
        compatibility = max(0, int(100 - distance * 12))
        st.metric(
            f"🤝 {selected_dong} × {c_dong} 궁합 점수",
            f"{compatibility}점",
            help="4축 z-score 거리 기반. 100점에 가까울수록 성격이 유사한 동네.",
        )

        # MBTI 케미 한줄평
        my_animal = MBTI_ANIMAL_NAMES.get(mbti, "")
        c_animal = MBTI_ANIMAL_NAMES.get(c_row["MBTI"], "")
        if compatibility >= 80:
            chem_emoji, chem_msg = "💕", f"{my_animal}와 {c_animal}, 찐친 케미! 이사 가도 어색함 ZERO"
        elif compatibility >= 60:
            chem_emoji, chem_msg = "😊", f"{my_animal}와 {c_animal}, 서로 다르지만 통하는 부분이 있어요"
        elif compatibility >= 40:
            chem_emoji, chem_msg = "🤔", f"{my_animal}와 {c_animal}, 적응 기간이 필요한 사이"
        elif compatibility >= 20:
            chem_emoji, chem_msg = "😅", f"{my_animal}와 {c_animal}, 꽤 다른 세계관… 충돌 주의"
        else:
            chem_emoji, chem_msg = "🔥", f"{my_animal}와 {c_animal}, 완전 반대! 오히려 끌리는 매력?"
        # 케미별 배경색
        if compatibility >= 80:
            chem_bg = "linear-gradient(135deg, rgba(243,156,18,0.08), rgba(231,76,60,0.06))"
        elif compatibility >= 60:
            chem_bg = "linear-gradient(135deg, rgba(39,174,96,0.06), rgba(52,152,219,0.06))"
        elif compatibility >= 40:
            chem_bg = "linear-gradient(135deg, rgba(149,165,166,0.08), rgba(127,140,141,0.06))"
        else:
            chem_bg = "linear-gradient(135deg, rgba(231,76,60,0.06), rgba(192,57,43,0.08))"
        st.markdown(
            f'<div class="chem-card" style="background:{chem_bg};">'
            f'{chem_emoji} <b>{mbti} × {c_row["MBTI"]} 케미:</b> {chem_msg}</div>',
            unsafe_allow_html=True,
        )

        # ── 캐릭터 대화 ──
        my_img = MBTI_ANIMALS.get(mbti, "")
        c_img = MBTI_ANIMALS.get(c_row["MBTI"], "")
        # 궁합별 말풍선 멘트
        if compatibility >= 80:
            my_say = f"우리 완전 통하잖아! 🥹"
            c_say = f"내 맘을 아는 동네 ✨"
        elif compatibility >= 60:
            my_say = f"좀 다르긴 한데… 괜찮은걸?"
            c_say = f"나도 그렇게 생각해 😏"
        elif compatibility >= 40:
            my_say = f"음… 적응하면 되겠지?"
            c_say = f"서로 노력하면 되지 뭐 😅"
        elif compatibility >= 20:
            my_say = f"여긴 좀 낯선데…?"
            c_say = f"우리 세계관이 다른 듯 🤨"
        else:
            my_say = f"완전 다른 세계다… 😳"
            c_say = f"그치만 끌리는걸? 🔥"
        st.markdown(f"""
        <div class="char-dialogue">
            <div class="char-dialogue-unit">
                <div class="char-bubble">{my_say}</div>
                <div style="filter:drop-shadow(0 3px 8px rgba(0,0,0,0.15));">{my_img}</div>
                <div class="char-dialogue-label">{selected_dong}<br><b>{mbti}</b> {my_animal}</div>
            </div>
            <div class="vs-icon">⚡</div>
            <div class="char-dialogue-unit">
                <div class="char-bubble">{c_say}</div>
                <div style="filter:drop-shadow(0 3px 8px rgba(0,0,0,0.15));">{c_img}</div>
                <div class="char-dialogue-label">{c_dong}<br><b>{c_row["MBTI"]}</b> {c_animal}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── 탭 1 → 탭 2 연결 CTA ──
    st.markdown("""
    <div class="next-tab-cta">
        <div class="next-tab-cta-icon">💬</div>
        <div class="next-tab-cta-text">
            <b>이 동네 말고 다른 조건으로 찾아볼래요?</b><br>
            <span>💬 동네 찾기 탭에서 AI에게 자연어로 질문해 보세요</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 탭 2: 자연어 동네 찾기 (Cortex Search + AI_COMPLETE)
# ════════════════════════════════════════════════════════════════════════════
import _snowflake
import json as _json
import re as _re

@st.cache_data(ttl=3600)
def _get_supported_sgg() -> frozenset:
    """DONG_PROFILES에서 지원 구 목록을 런타임 조회 → 구 추가 시 코드 수정 불필요."""
    rows = session.sql(
        "SELECT DISTINCT SGG FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES ORDER BY SGG"
    ).to_pandas()
    return frozenset(rows["SGG"].tolist())


def _check_unsupported_district(query: str):
    """지원 범위 외 구 언급 감지 → 안내 메시지 반환, 없으면 None."""
    supported = _get_supported_sgg()
    found = _re.findall(r'\S+구', query)
    unsupported = [s for s in found if s not in supported]
    if unsupported:
        names = "·".join(unsupported)
        supported_str = "·".join(sorted(supported))
        return (
            f"죄송해요! **{names}**는 현재 서비스 범위에 없어요. "
            f"동네 MBTI는 **{supported_str}** {len(supported)}개 구만 지원합니다. "
            f"이 중 하나로 다시 질문해 주세요! 😊"
        )
    return None


def _extract_sgg(query: str):
    """쿼리에서 구 이름 감지."""
    for sgg in _get_supported_sgg():
        if sgg in query:
            return sgg
    return None


def _cortex_search(query: str, sgg_filter: str = None) -> list:
    """Cortex Search REST 호출 → 동네 프로필 리스트 반환. 실패 시 SQL ILIKE 폴백."""
    body = {
        "query": query,
        "columns": ["SGG", "EMD", "MBTI", "CHARACTER_SUMMARY", "PROFILE_TEXT"],
        "limit": 5,
    }
    if sgg_filter:
        body["filter"] = {"@eq": {"SGG": sgg_filter}}

    try:
        resp = _snowflake.send_snow_api_request(
            "POST",
            "/api/v2/databases/DONGNE_MBTI/schemas/PUBLIC/cortex-search-services/DONGNE_SEARCH:query",
            {}, {},
            body,
            None,
            30000,
        )
        if resp.get("status") == 200:
            data = _json.loads(resp.get("content", "{}"))
            results = data.get("results", [])
            if results:
                return results
    except Exception:
        pass

    # SQL ILIKE 폴백 (Cortex Search 실패 시)
    try:
        kw = query.replace("'", "''")
        sgg_cond = f"AND SGG = '{sgg_filter}'" if sgg_filter else ""
        rows = session.sql(f"""
            SELECT SGG, EMD, MBTI, CHARACTER_SUMMARY, PROFILE_TEXT
            FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES
            WHERE (PROFILE_TEXT ILIKE '%{kw}%'
               OR CHARACTER_SUMMARY ILIKE '%{kw}%'
               OR MBTI ILIKE '%{kw}%')
            {sgg_cond}
            LIMIT 5
        """).to_pandas()
        return rows.to_dict("records")
    except Exception:
        return []


def _search_and_respond(query: str, history: list = None) -> tuple:
    """Cortex Search → AI_COMPLETE(llama3.3-70b) 멀티턴 대화 답변 생성."""
    sgg = _extract_sgg(query)
    results = _cortex_search(query, sgg_filter=sgg)

    if results:
        context = "\n".join([
            f"- {r.get('SGG','')} {r.get('EMD','')}동 (MBTI: {r.get('MBTI','')}): {r.get('CHARACTER_SUMMARY','')}"
            for r in results
        ])
        no_data = False
    else:
        context = "검색 결과 없음"
        no_data = True

    system_msg = (
        "당신은 서울 동네 MBTI 전문가입니다. "
        "주어진 데이터만 기반으로 답변하고, 데이터에 없는 내용은 지어내지 마세요. "
        "이전 대화 맥락을 유지하며 자연스럽게 이어서 답변하세요."
    )
    current_user_msg = (
        f"질문: {query}\n\n"
        + (
            f"검색된 동네 데이터:\n{context}\n\n"
            "위 동네들의 특성을 바탕으로 3문장 이내로 친근하게 답변해주세요. "
            "동네 이름과 MBTI를 반드시 언급하세요."
            if not no_data else
            "서초구·영등포구·중구 데이터에서 관련 동네를 찾지 못했습니다. "
            "솔직하게 찾지 못했다고 안내하고 다른 질문을 유도해주세요."
        )
    )

    # 멀티턴: 이전 대화 히스토리 → ARRAY_CONSTRUCT에 순서대로 삽입
    history_sql_parts = []
    for msg in (history or []):
        role = "user" if msg["role"] == "user" else "assistant"
        content = msg["content"].replace("'", "\\'")
        history_sql_parts.append(
            f"OBJECT_CONSTRUCT('role', '{role}', 'content', '{content}')"
        )

    system_msg_esc = system_msg.replace("'", "\\'")
    current_user_msg_esc = current_user_msg.replace("'", "\\'")

    all_messages = (
        [f"OBJECT_CONSTRUCT('role', 'system', 'content', '{system_msg_esc}')"]
        + history_sql_parts
        + [f"OBJECT_CONSTRUCT('role', 'user', 'content', '{current_user_msg_esc}')"]
    )
    messages_sql = ", ".join(all_messages)

    try:
        answer = session.sql(f"""
            SELECT AI_COMPLETE(
                '{MODEL_PRIMARY}',
                ARRAY_CONSTRUCT({messages_sql})
            )
        """).collect()[0][0]
    except Exception as e:
        # Primary 실패 시 Fallback 모델로 재시도 (히스토리 없이 단순 호출)
        try:
            fallback_prompt = f"{system_msg}\n\n{current_user_msg}".replace("'", "''")
            answer = session.sql(
                f"SELECT AI_COMPLETE('{MODEL_FALLBACK}', '{fallback_prompt}')"
            ).collect()[0][0]
        except Exception as e2:
            answer = f"응답 생성 오류: {str(e2)[:100]}"

    return answer, results


with tab2:
    st.markdown("""
    <div class="tab-header">
        <h3>💬 자연어로 동네 찾기</h3>
        <p>Cortex Search + AI가 118개 동에서 딱 맞는 동네를 찾아드려요</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        f'<div class="info-card">'
        f'🔍 <b>작동 방식</b>: 질문 → Cortex Search로 관련 동네 검색 → '
        f'AI({MODEL_PRIMARY})가 맞춤 답변 생성</div>',
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ── 추천 질문 버튼 (대화 시작 전에만 표시) ──
    if not st.session_state.messages:
        SUGGESTIONS = [
            "조용하고 안정적인 동네 어디야?",
            "젊고 활발한 분위기 동네 추천해줘",
            "서초구에서 부유한 동네 알려줘",
            "반포동이랑 비슷한 동네 찾아줘",
        ]
        st.markdown("**빠른 질문:**")
        col_a, col_b = st.columns(2)
        for i, sug in enumerate(SUGGESTIONS):
            col = col_a if i % 2 == 0 else col_b
            if col.button(sug, key=f"sug_{i}", use_container_width=True):
                st.session_state["_pending"] = sug
                st.experimental_rerun()

    # ── 대화 히스토리 출력 ──
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-msg chat-msg-user">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-msg chat-msg-ai">🤖 {msg["content"]}</div>',
                unsafe_allow_html=True,
            )

    # ── 채팅 입력 (Enter 전송 + 전송 후 자동 비우기) ──
    prompt = st.session_state.pop("_pending", None)
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            text_in = st.text_input(
                "질문 입력",
                placeholder="예: 서초구에서 조용하고 부유한 동네 추천해줘",
                label_visibility="collapsed",
            )
        with col_btn:
            send = st.form_submit_button("전송", use_container_width=True)

    if send and text_in:
        prompt = text_in

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        unsupported = _check_unsupported_district(prompt)
        if unsupported:
            st.session_state.messages.append({"role": "assistant", "content": unsupported})
        else:
            with st.spinner("동네를 찾고 있어요..."):
                # 현재 질문 제외한 이전 대화만 히스토리로 전달 (마지막 user 메시지는 함수 내에서 처리)
                prev_history = st.session_state.messages[:-1]
                answer_text, _ = _search_and_respond(prompt, history=prev_history)
            st.session_state.messages.append({"role": "assistant", "content": answer_text})
        st.experimental_rerun()

    if st.session_state.messages:
        if st.button("대화 초기화", key="reset_chat"):
            st.session_state.messages = []
            st.experimental_rerun()

    # ── 탭 2 → 탭 3 연결 CTA ──
    st.markdown("""
    <div class="next-tab-cta">
        <div class="next-tab-cta-icon">📊</div>
        <div class="next-tab-cta-text">
            <b>후보 동네의 집값 트렌드가 궁금하다면?</b><br>
            <span>📊 시세 전망 탭에서 실거래가 추이와 ML 예측을 확인하세요</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 탭 3: 동네 시세 전망 (ML FORECAST + 인구 흐름 + AI 종합 분석)
# ════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=3600)
def load_forecast(sgg: str, emd: str):
    """PRICE_FORECAST_RESULT에서 ML 예측값 로드 (3개월 사전 계산, fallback)."""
    dong_id = f"{sgg}_{emd}"
    try:
        return session.sql(f"""
            SELECT TS, FORECAST AS FORECAST_PRICE,
                   LOWER_BOUND, UPPER_BOUND
            FROM DONGNE_MBTI.PUBLIC.PRICE_FORECAST_RESULT
            WHERE SERIES = '{dong_id}'
            ORDER BY TS
        """).to_pandas()
    except Exception:
        return pd.DataFrame()


def _get_dynamic_forecast(n_periods: int, sgg: str, emd: str):
    """FORECAST 모델 실시간 호출 — session_state 캐시."""
    cache_key = f"_fc_{n_periods}"
    if cache_key not in st.session_state:
        try:
            df = session.sql(f"""
                CALL DONGNE_MBTI.PUBLIC.PRICE_FORECAST!FORECAST(
                    FORECASTING_PERIODS => {int(n_periods)}
                )
            """).to_pandas()
            # SiS quoted identifier 정규화
            df.columns = [c.strip('"').upper() for c in df.columns]
            st.session_state[cache_key] = df
        except Exception:
            st.session_state[cache_key] = pd.DataFrame()

    all_df = st.session_state[cache_key]
    if all_df.empty:
        return pd.DataFrame()

    dong_id = f"{sgg}_{emd}"
    # SERIES 값은 '"서초구_반포동"' 형태 (따옴표 포함)
    mask = all_df["SERIES"].astype(str).str.strip('"') == dong_id
    result = all_df.loc[mask, ["TS", "FORECAST", "LOWER_BOUND", "UPPER_BOUND"]].copy()
    if not result.empty:
        result = result.rename(columns={"FORECAST": "FORECAST_PRICE"})
    return result


@st.cache_data(ttl=3600)
def _load_population_movement(sgg: str):
    """인구이동 데이터 — DB 없으면 graceful skip."""
    try:
        return session.sql(f"""
            SELECT MOVEMENT_TYPE, SUM(POPULATION) AS TOTAL
            FROM KOREA_REAL_ESTATE_APARTMENT_MARKET_INTELLIGENCE
                .HACKATHON_2026.REGION_POPULATION_MOVEMENT
            WHERE SGG = '{sgg}' AND YYYYMMDD >= '2021-01-01'
            GROUP BY MOVEMENT_TYPE
        """).to_pandas()
    except Exception:
        return pd.DataFrame()


_DOMAIN_CONTEXT = {
    "서초구": "서초구는 의료/뷰티 인프라 허브이자 고소득 주거지로, 강남 생활권의 핵심입니다.",
    "영등포구": "영등포구는 여의도 직장 접근성과 교통 허브로, 직주근접 수요가 안정적입니다.",
    "중구": "중구는 도심 상업지로, 직주근접 가치와 관광/상업 인프라가 강점입니다.",
}


with tab3:
    st.markdown("""
    <div class="tab-header">
        <h3>📊 동네 시세 전망</h3>
        <p>실거래가 추이 + ML 장기 예측 + 인구 흐름 + AI 종합 분석으로 매매 타이밍을 판단하세요</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 구/동 선택 + 예측 기간 ──
    sel1, sel2 = st.columns([1, 2])
    with sel1:
        t3_gu = st.selectbox("구 선택 ", sorted(load_mbti_result()["SGG"].unique()), key="t3_gu")
    with sel2:
        t3_dong_list = sorted(load_mbti_result()[load_mbti_result()["SGG"] == t3_gu]["EMD"].unique())
        t3_dong = st.selectbox("동 선택 ", t3_dong_list, key="t3_dong")

    forecast_period = st.radio(
        "예측 기간",
        ["3개월", "12개월", "36개월", "60개월 (5년)"],
        horizontal=True,
        index=0,
        key="t3_fc_period",
    )
    _PERIOD_MAP = {"3개월": 3, "12개월": 12, "36개월": 36, "60개월 (5년)": 60}
    n_periods = _PERIOD_MAP[forecast_period]

    price_df = load_price_history(t3_gu, t3_dong)

    # 개인화 섹션에서 참조할 변수 초기화 (price_df 비어있어도 안전)
    has_forecast = False
    forecast_df = pd.DataFrame()
    latest = 0
    pop_net = None
    price_delta = 0

    if price_df.empty:
        st.info(f"📭 {t3_gu} {t3_dong}의 아파트 실거래가 데이터가 없습니다.")
    else:
        price_df["YYYYMMDD"] = pd.to_datetime(price_df["YYYYMMDD"].astype(str), errors="coerce")
        price_df = price_df.dropna(subset=["YYYYMMDD"]).sort_values("YYYYMMDD")

        # ── ML 예측 로드 (실시간 CALL + 3개월 사전계산 fallback) ──
        # 캐시는 전체 시리즈를 n_periods별로 1회 저장, Python에서 dong 필터
        if f"_fc_{n_periods}" not in st.session_state:
            with st.spinner(f"ML 모델이 {forecast_period} 예측 중..."):
                forecast_df = _get_dynamic_forecast(n_periods, t3_gu, t3_dong)
        else:
            forecast_df = _get_dynamic_forecast(n_periods, t3_gu, t3_dong)

        fc_fallback = False
        if forecast_df.empty:
            forecast_df = load_forecast(t3_gu, t3_dong)
            if not forecast_df.empty and n_periods != 3:
                fc_fallback = True

        has_forecast = not forecast_df.empty

        if has_forecast:
            forecast_df = forecast_df.copy()
            forecast_df["TS"] = pd.to_datetime(forecast_df["TS"])
            forecast_df["FORECAST_PRICE"] = pd.to_numeric(forecast_df["FORECAST_PRICE"], errors="coerce")
            forecast_df["LOWER_BOUND"] = pd.to_numeric(forecast_df["LOWER_BOUND"], errors="coerce").fillna(forecast_df["FORECAST_PRICE"])
            forecast_df["UPPER_BOUND"] = pd.to_numeric(forecast_df["UPPER_BOUND"], errors="coerce").fillna(forecast_df["FORECAST_PRICE"])
            # coercion 후 전체 NaN이면 예측 없음으로 처리
            if forecast_df["FORECAST_PRICE"].isna().all():
                has_forecast = False
                forecast_df = pd.DataFrame()

        if fc_fallback:
            st.caption("⚠️ 실시간 예측이 불가하여 사전 계산된 3개월 예측을 표시합니다.")

        # ── 통합 차트: 실거래 + ML 예측 (temporal X축 통일) ──
        fc_label = f"향후 {n_periods}개월" if has_forecast and not fc_fallback else ("향후 3개월 (fallback)" if fc_fallback else "")
        st.markdown(f"**📈 시세 추이 & ML 예측** {fc_label}")

        # 과거 데이터
        past_chart = price_df[["YYYYMMDD", "AVG_PRICE"]].rename(
            columns={"YYYYMMDD": "TS", "AVG_PRICE": "PRICE"}
        ).copy()
        past_chart["TYPE"] = "실거래"
        past_chart["LOWER"] = past_chart["PRICE"]
        past_chart["UPPER"] = past_chart["PRICE"]

        if has_forecast:
            future_chart = forecast_df[["TS", "FORECAST_PRICE", "LOWER_BOUND", "UPPER_BOUND"]].rename(
                columns={"FORECAST_PRICE": "PRICE", "LOWER_BOUND": "LOWER", "UPPER_BOUND": "UPPER"}
            ).copy()
            future_chart["TYPE"] = "ML 예측"
            combined = pd.concat([past_chart, future_chart], ignore_index=True).sort_values("TS")
        else:
            combined = past_chart.copy()

        today_ts = price_df["YYYYMMDD"].max()

        # 호버 셀렉션
        nearest = alt.selection_single(nearest=True, on="mouseover", fields=["TS"], empty="none")

        # Layer 1: 과거 실선 (파란)
        past_data = combined[combined["TYPE"] == "실거래"]
        past_line = alt.Chart(past_data).mark_line(
            color="#60A5FA", strokeWidth=2.5
        ).encode(
            x=alt.X("TS:T", title="",
                     axis=alt.Axis(format="%y년 %m월", labelAngle=-45, tickCount=10)),
            y=alt.Y("PRICE:Q", title="평당가 (만원)", scale=alt.Scale(zero=False)),
        )

        layers = [past_line]

        if has_forecast:
            fc_data = combined[combined["TYPE"] == "ML 예측"]

            # Layer 2: 신뢰구간 band (빨강 반투명)
            fc_band = alt.Chart(fc_data).mark_area(
                opacity=0.12, color="#F87171"
            ).encode(
                x="TS:T",
                y=alt.Y("LOWER:Q", title=""),
                y2="UPPER:Q",
            )
            layers.append(fc_band)

            # Layer 3: 예측 대시 라인 (빨강)
            fc_line = alt.Chart(fc_data).mark_line(
                color="#F87171", strokeWidth=2.5, strokeDash=[6, 4]
            ).encode(x="TS:T", y="PRICE:Q")
            layers.append(fc_line)

            # Layer 4: 오늘 기준선 (회색 점선)
            today_rule = alt.Chart(pd.DataFrame({"x": [today_ts]})).mark_rule(
                color="#9CA3AF", strokeDash=[4, 4], strokeWidth=1.5
            ).encode(x="x:T")
            layers.append(today_rule)

        # Layer 5: 호버 포인트 (전체 데이터)
        hover_pts = alt.Chart(combined).mark_circle(size=60).encode(
            x="TS:T",
            y="PRICE:Q",
            color=alt.condition(
                alt.datum.TYPE == "실거래",
                alt.value("#60A5FA"),
                alt.value("#F87171"),
            ),
            opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
            tooltip=[
                alt.Tooltip("TS:T", title="날짜", format="%Y년 %m월"),
                alt.Tooltip("PRICE:Q", title="평당가", format=",.0f"),
                alt.Tooltip("TYPE:N", title="구분"),
            ],
        ).add_selection(nearest)
        layers.append(hover_pts)

        # Layer 6: 크로스헤어 룰
        crosshair = alt.Chart(combined).mark_rule(
            color="gray", strokeDash=[4, 4]
        ).encode(
            x="TS:T",
            opacity=alt.condition(nearest, alt.value(0.5), alt.value(0)),
        ).transform_filter(nearest)
        layers.append(crosshair)

        chart = alt.layer(*layers).properties(height=400).configure_view(strokeWidth=0)
        st.altair_chart(chart, use_container_width=True)

        # ── 메트릭 ──
        latest = price_df.iloc[-1]["AVG_PRICE"]
        if len(price_df) >= 2:
            prev = price_df.iloc[-2]["AVG_PRICE"]
            price_delta = latest - prev
        else:
            price_delta = 0

        if has_forecast:
            m1, m2, m3 = st.columns(3)
            pred_latest = forecast_df["FORECAST_PRICE"].iloc[-1]
            pred_delta = pred_latest - latest
            pct_change = (pred_latest - latest) / latest * 100 if latest > 0 else 0
            fc_end = forecast_df["TS"].max().strftime("%Y.%m")
            m1.metric("최근 평당가", f"{latest:,.0f}만원", f"{price_delta:+,.0f}만원")
            m2.metric(f"예측가 ({fc_end})", f"{pred_latest:,.0f}만원", f"{pred_delta:+,.0f}만원")
            m3.metric("예측 변화율", f"{pct_change:+.1f}%")
        else:
            m1, m2 = st.columns(2)
            m1.metric("최근 평당가", f"{latest:,.0f}만원", f"{price_delta:+,.0f}만원")
            m2.metric("데이터 기간", f"{price_df['YYYYMMDD'].iloc[0].strftime('%Y.%m')} ~ {price_df['YYYYMMDD'].iloc[-1].strftime('%Y.%m')}")

        # ── 인구 흐름 (compact — graceful skip) ──
        pop_df = _load_population_movement(t3_gu)
        pop_net = None
        if not pop_df.empty:
            try:
                net_row = pop_df[pop_df["MOVEMENT_TYPE"] == "순이동"]
                if not net_row.empty and pd.notna(net_row["TOTAL"].iloc[0]):
                    pop_net = int(net_row["TOTAL"].iloc[0])
                    direction = "전입 우세 — 수요 지속" if pop_net > 0 else "전출 우세 — 수요 약화"
                    st.metric(
                        "👥 최근 5년 인구 흐름",
                        f"순이동 {pop_net:+,}명",
                        direction,
                        delta_color="normal" if pop_net > 0 else "inverse",
                    )
            except Exception:
                pass

        # ── AI 종합 전망 (자동 생성, session_state 캐시) ──
        st.divider()
        st.markdown("**🤖 AI 종합 전망**")

        ai_key = f"_ai_{t3_gu}_{t3_dong}_{n_periods}"
        if ai_key not in st.session_state:
            with st.spinner("AI가 시세·인구·지역 데이터를 종합 분석 중..."):
                try:
                    recent_prices = price_df.tail(6)["AVG_PRICE"].tolist()

                    # 시세 정보
                    ml_info = ""
                    if has_forecast:
                        fc_end_str = forecast_df["TS"].max().strftime("%Y년 %m월")
                        fc_pct = (forecast_df["FORECAST_PRICE"].iloc[-1] - latest) / latest * 100
                        ml_info = (
                            f"\n- ML {n_periods}개월 예측 ({fc_end_str}까지): "
                            f"최종 {forecast_df['FORECAST_PRICE'].iloc[-1]:,.0f}만원 (변화율 {fc_pct:+.1f}%)"
                            f"\n- 90% 신뢰구간: {forecast_df['LOWER_BOUND'].iloc[-1]:,.0f}"
                            f" ~ {forecast_df['UPPER_BOUND'].iloc[-1]:,.0f}만원"
                        )

                    # 인구 정보
                    pop_info = ""
                    if pop_net is not None:
                        flow_dir = "전입 우세" if pop_net > 0 else "전출 우세"
                        pop_info = f"\n\n[인구 흐름]\n- 최근 5년 순이동: {pop_net:+,}명 ({flow_dir})"

                    # 지역 특성
                    domain_ctx = _DOMAIN_CONTEXT.get(t3_gu, f"{t3_gu} 지역입니다.")

                    # 6개월 변화율 계산
                    p_first, p_last = recent_prices[0], recent_prices[-1]
                    p_6m_pct = (p_last - p_first) / p_first * 100 if p_first > 0 else 0

                    prompt = (
                        f"반드시 한국어로 답변하세요. 영어 사용 금지.\n"
                        f"당신은 서울 부동산 시장 10년차 전문 분석가입니다. "
                        f"KB부동산 리서치 보고서 수준의 전문 분석 리포트를 작성하세요.\n\n"
                        f"[시세 데이터]\n"
                        f"- {t3_gu} {t3_dong} 최근 6개월 평당가 추이: "
                        f"{[round(p) for p in recent_prices]}만원\n"
                        f"- 6개월 변화율: {p_6m_pct:+.1f}%\n"
                        f"- 최근 평당가: {round(recent_prices[-1])}만원"
                        f"{ml_info}"
                        f"{pop_info}\n\n"
                        f"[지역 특성]\n- {domain_ctx}\n\n"
                        f"[출력 형식 — 반드시 아래 3단 구조로 작성. 각 섹션 제목을 그대로 사용.]\n\n"
                        f"📈 시세 트렌드 분석\n"
                        f"- 최근 6개월 평당가 흐름을 월별로 상세 분석 (시작가→현재가, 변화율)\n"
                        f"- ML 예측 모델 결과를 인용하여 향후 시세 방향 전망\n"
                        f"- 현재 시세가 상승/하락/보합 중 어느 국면인지 전문가 판단\n"
                        f"- 서울 전체 또는 해당 구 평균 대비 이 동네의 위치 언급\n"
                        f"- 3-4문장으로 작성\n\n"
                        f"📊 수요·입지 분석\n"
                        f"- 인구 순이동 데이터를 근거로 실수요 강도 판단 (있을 때만)\n"
                        f"- 해당 지역의 입지 특성 (교통, 인프라, 생활권) 분석\n"
                        f"- 수요 강세/약세 신호를 종합하여 실수요 전망\n"
                        f"- 3-4문장으로 작성\n\n"
                        f"💡 투자 판단 및 전략\n"
                        f"- 위 시세 트렌드 + 수요 분석을 종합\n"
                        f"- 매수/매도/관망 중 하나를 명확히 제시\n"
                        f"- 해당 판단의 핵심 근거 2가지를 숫자와 함께 제시\n"
                        f"- 매수라면 적정 진입 시점/전략, 관망이라면 주시할 지표 제안\n"
                        f"- 2-3문장으로 작성\n\n"
                        f"[필수 규칙]\n"
                        f"- 모든 숫자에 단위(만원, %, 명) 포함\n"
                        f"- '다양한', '좋은 환경', '편리한 교통' 같은 일반론 금지\n"
                        f"- 반드시 위 데이터의 구체 숫자를 인용하여 분석\n"
                        f"- 전문 분석가의 리포트답게 객관적이고 논리적으로 작성"
                    )
                    # $$ delimiter로 SQL 인젝션 안전하게 처리
                    safe_prompt = prompt.replace("$$", "")
                    ai_result = session.sql(
                        f"SELECT AI_COMPLETE('{MODEL_PRIMARY}', $${safe_prompt}$$) AS FORECAST"
                    ).collect()[0]["FORECAST"]
                    st.session_state[ai_key] = ai_result if ai_result else ""
                except Exception as e:
                    st.session_state[ai_key] = f"__ERR__{str(e)[:150]}"

        cached_ai = st.session_state.get(ai_key, "")
        if cached_ai.startswith("__ERR__"):
            st.error(f"AI 전망 생성 중 오류: {cached_ai[7:]}")
        elif cached_ai:
            # AI 응답 정리: 따옴표 제거 + 리터럴 \n → 실제 줄바꿈
            clean_ai = cached_ai.strip().strip('"').replace("\\n", "\n")
            st.markdown(clean_ai)
        else:
            st.info("AI 전망을 생성할 수 없습니다.")

    # ── 🧬 성격 × 이 동네 (개인화 reveal / 퀴즈 CTA) ──
    # 변수 초기화 (line 1612)로 price_df 비어있어도 안전
    st.divider()
    _AXIS_INTERPRET = {
        "EI": {True: "외향적·활동적 성향", False: "내향적·조용한 성향"},
        "SN": {True: "문화적·감각적 성향", False: "실용적·현실적 성향"},
        "TF": {True: "이성적·투자 중시 성향", False: "감성적·생활 만족 중시 성향"},
        "JP": {True: "변화 수용적 성향", False: "안정 추구 성향"},
    }

    if st.session_state.get("quiz_user_mbti"):
        # ── 퀴즈 완료: 개인화 섹션 ──
        st.markdown("**🧬 당신의 성격 × 이 동네**")
        st.caption("퀴즈 결과 + 시세 예측 + 인구 흐름 + 동네 성격을 AI가 종합 판단합니다")

        user_mbti = st.session_state.quiz_user_mbti
        user_scores = st.session_state.quiz_user_scores
        profiles_df = load_profiles()
        dong_row = profiles_df[
            (profiles_df["SGG"] == t3_gu) & (profiles_df["EMD"] == t3_dong)
        ]

        if dong_row.empty:
            pass  # 동네 프로필 없으면 개인화 섹션 숨김
        else:
            dong_info = dong_row.iloc[0]
            dong_mbti = dong_info.get("MBTI", "")
            dong_sentiment = dong_info.get("SENTIMENT_SCORE", None)
            dong_type = dong_info.get("NEIGHBORHOOD_TYPE", "")

            # 축별 해석 생성
            user_tf = user_scores.get("TF", 0)
            user_jp = user_scores.get("JP", 0)
            tf_text = _AXIS_INTERPRET["TF"][user_tf > 0]
            jp_text = _AXIS_INTERPRET["JP"][user_jp > 0]

            # MBTI 뱃지 표시 (수치 대신 투자 스타일 표현)
            ei_text = _AXIS_INTERPRET["EI"][user_scores.get("EI", 0) > 0]
            sn_text = _AXIS_INTERPRET["SN"][user_scores.get("SN", 0) > 0]
            style_tags = f"{ei_text} · {tf_text}"  # 핵심 2개 축만 표시
            st.markdown(
                f'<div class="info-card">'
                f'👤 나의 투자 스타일: <b>{user_mbti}</b> '
                f'({style_tags})'
                f'&nbsp;&nbsp;↔&nbsp;&nbsp;'
                f'🏘️ 동네 성격: <b>{dong_mbti}</b> ({dong_type})'
                f'</div>',
                unsafe_allow_html=True,
            )

            # AI 개인화 조언 (session_state 캐시)
            fit_key = f"_ai_fit_{t3_gu}_{t3_dong}_{n_periods}"
            if fit_key not in st.session_state:
                with st.spinner("AI가 당신의 성격과 이 동네의 미래를 매칭 중..."):
                    try:
                        # 시세/인구 정보 (Tab 3 기존 변수 재사용)
                        price_info = ""
                        if has_forecast:
                            fc_pct = (forecast_df["FORECAST_PRICE"].iloc[-1] - latest) / latest * 100 if latest > 0 else 0
                            price_info = f"\n- ML {n_periods}개월 시세 예측: {fc_pct:+.1f}%"

                        pop_info = ""
                        if pop_net is not None:
                            flow_dir = "전입 우세" if pop_net > 0 else "전출 우세"
                            pop_info = f"\n- 인구 순이동: {pop_net:+,}명 ({flow_dir})"

                        sentiment_info = ""
                        if dong_sentiment is not None and str(dong_sentiment) not in ("None", "nan", ""):
                            sent_val = float(dong_sentiment)
                            sent_label = "긍정적" if sent_val > 0 else "부정적" if sent_val < 0 else "중립"
                            sentiment_info = f"\n- 동네 감성 점수: {sent_val:+.2f} ({sent_label})"

                        domain_ctx = _DOMAIN_CONTEXT.get(t3_gu, f"{t3_gu} 지역입니다.")

                        fit_prompt = (
                            f"반드시 한국어로 답변하세요. 영어 사용 금지.\n\n"
                            f"당신은 10년 경력의 부동산 컨설턴트이자 사용자의 오래된 친구입니다. "
                            f"전문 지식을 갖추고 있지만, 친구에게 말하듯 편하게 조언해주세요.\n\n"
                            f"[사용자 투자 스타일]\n"
                            f"- {tf_text}\n"
                            f"  → {'일상의 만족도, 동네 분위기, 편의시설 접근성이 시세보다 중요' if user_tf <= 0 else '자산 가치 상승 가능성과 투자 수익률을 최우선으로 고려'}\n"
                            f"- {jp_text}\n"
                            f"  → {'새로운 동네에서 새 라이프스타일을 시작하는 것에 거부감 없음' if user_jp > 0 else '이미 검증된, 안정적이고 예측 가능한 동네를 선호'}\n\n"
                            f"[이 동네 정보]\n"
                            f"- {t3_gu} {t3_dong}: {dong_type}"
                            f"{price_info}"
                            f"{pop_info}"
                            f"{sentiment_info}\n\n"
                            f"[지역 특성]\n- {domain_ctx}\n\n"
                            f"[출력 형식]\n"
                            f"4-6문장의 자연스러운 조언을 작성하세요:\n"
                            f"- 첫 문장: '당신은 ~한 스타일이니까' 로 시작\n"
                            f"- 중간: 이 동네의 특성이 사용자 스타일과 어떻게 맞거나 안 맞는지 구체적으로 설명\n"
                            f"  (예: 생활 중시 스타일이면 이 동네의 인프라/분위기를 중심으로,\n"
                            f"   투자 중시 스타일이면 시세 상승률/수요를 중심으로)\n"
                            f"- 마지막: 매수/관망/매도 판단 + '당신 스타일에는' 이유\n\n"
                            f"[필수 규칙]\n"
                            f"- 친구에게 말하듯 편한 어투 (~해, ~거야, ~것 같아)\n"
                            f"- 다른 투자 스타일이면 완전히 다른 조언이 나와야 함\n"
                            f"- 숫자를 직접 나열하지 말고 해석해서 전달 (예: '시세가 꾸준히 오르고 있어')\n"
                            f"- 동네 이름과 구체적 특성을 언급하여 맞춤 느낌 강화"
                        )
                        safe_prompt = fit_prompt.replace("$$", "")
                        ai_fit = session.sql(
                            f"SELECT AI_COMPLETE('{MODEL_PRIMARY}', $${safe_prompt}$$) AS RESULT"
                        ).collect()[0]["RESULT"]
                        st.session_state[fit_key] = ai_fit if ai_fit else ""
                    except Exception as e:
                        st.session_state[fit_key] = f"__ERR__{str(e)[:150]}"

            cached_fit = st.session_state.get(fit_key, "")
            if cached_fit.startswith("__ERR__"):
                st.error(f"맞춤 분석 생성 중 오류: {cached_fit[7:]}")
            elif cached_fit:
                clean_fit = cached_fit.strip().strip('"').replace("\\n", "\n")
                st.markdown(
                    f'<div class="chat-msg chat-msg-ai">🧬 {clean_fit}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.info("맞춤 분석을 생성할 수 없습니다.")
    else:
        # ── 퀴즈 미완료: CTA ──
        st.markdown("""
        <div class="info-card">
            <b>🧬 나에게 맞는 맞춤 분석을 받으려면?</b><br>
            성향 테스트를 완료하면, 당신의 성격에 맞는 <b>개인화된 투자 조언</b>을 받을 수 있어요.<br>
            같은 동네라도 성격에 따라 다른 조언이 나옵니다.
        </div>
        """, unsafe_allow_html=True)

    # ── 탭 3 → 탭 4 연결 CTA ──
    st.markdown("""
    <div class="next-tab-cta">
        <div class="next-tab-cta-icon">🔬</div>
        <div class="next-tab-cta-text">
            <b>더 구체적인 데이터 비교가 필요하다면?</b><br>
            <span>🔬 데이터 탐색 탭에서 후보 동네들을 한번에 비교하세요</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 탭 4: 데이터 탐색 — Cortex Analyst (NL2SQL)
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="tab-header">
        <h3>🔬 Cortex Analyst — 데이터 탐색</h3>
        <p>자연어 질문을 SQL로 자동 변환하여 MBTI 점수·통계·순위를 조회합니다</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        '<div class="info-card">'
        '📊 <b>Cortex Analyst</b>: 텍스트 검색(탭2)과 달리, 수치 데이터를 정확하게 조회합니다. '
        '"TOP 3", "평균", "비교" 같은 데이터 질의에 최적화.</div>',
        unsafe_allow_html=True,
    )

    _ANALYST_SEMANTIC_MODEL = (
        "@DONGNE_MBTI.PUBLIC.DONGNE_REPO/branches/main/models/dongne_mbti.yaml"
    )
    _ANALYST_EXAMPLES = [
        "서초구에서 가장 외향적인(E) 동네 TOP 3 알려줘",
        "ISTJ 유형인 동네 목록 보여줘",
        "각 구별 평균 TF 점수 비교해줘",
        "영등포구에서 변화(P) 성향이 가장 강한 동네는?",
        "16개 MBTI 유형 분포가 어떻게 돼?",
    ]

    # 예시 질문 버튼
    if not st.session_state.get("analyst_history"):
        st.markdown("**예시 질문:**")
        ex_row1 = st.columns(3)
        ex_row2 = st.columns(2)
        for i, ex in enumerate(_ANALYST_EXAMPLES):
            col = ex_row1[i] if i < 3 else ex_row2[i - 3]
            if col.button(ex, key=f"analyst_ex_{i}", use_container_width=True):
                st.session_state["_analyst_pending"] = ex
                st.experimental_rerun()

    # 대화 히스토리 출력
    for msg in st.session_state.get("analyst_history", []):
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-msg chat-msg-user">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-msg chat-msg-ai">📊 {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
            if msg.get("sql"):
                with st.expander("생성된 SQL 보기"):
                    st.code(msg["sql"], language="sql")
            if msg.get("data") is not None:
                st.dataframe(msg["data"], use_container_width=True)

    # 입력 폼
    analyst_prompt = st.session_state.pop("_analyst_pending", None)
    with st.form(key="analyst_form", clear_on_submit=True):
        a_col1, a_col2 = st.columns([5, 1])
        with a_col1:
            analyst_input = st.text_input(
                "Analyst 질문",
                placeholder="예: 서초구에서 가장 부유한(T) 동네 TOP 5는?",
                label_visibility="collapsed",
            )
        with a_col2:
            analyst_send = st.form_submit_button("조회", use_container_width=True)

    if analyst_send and analyst_input:
        analyst_prompt = analyst_input

    if analyst_prompt:
        if "analyst_history" not in st.session_state:
            st.session_state.analyst_history = []
        st.session_state.analyst_history.append({"role": "user", "content": analyst_prompt})

        with st.spinner("Cortex Analyst가 SQL을 생성하고 있어요..."):
            try:
                analyst_body = {
                    "messages": [
                        {"role": "user", "content": [{"type": "text", "text": analyst_prompt}]}
                    ],
                    "semantic_model_file": _ANALYST_SEMANTIC_MODEL,
                }
                resp = _snowflake.send_snow_api_request(
                    "POST",
                    "/api/v2/cortex/analyst/message",
                    {}, {},
                    analyst_body,
                    None,
                    30000,
                )
                if resp.get("status") == 200:
                    resp_data = _json.loads(resp.get("content", "{}"))
                    content_blocks = resp_data.get("message", {}).get("content", [])

                    analyst_text = ""
                    analyst_sql = ""
                    for block in content_blocks:
                        if block.get("type") == "text":
                            analyst_text = block.get("text", "")
                        elif block.get("type") == "sql":
                            analyst_sql = block.get("statement", "")

                    # SQL 실행하여 결과 표시
                    result_df = None
                    if analyst_sql:
                        try:
                            result_df = session.sql(analyst_sql).to_pandas()
                        except Exception:
                            result_df = None

                    st.session_state.analyst_history.append({
                        "role": "analyst",
                        "content": analyst_text or "SQL을 생성했습니다.",
                        "sql": analyst_sql,
                        "data": result_df,
                    })
                else:
                    st.session_state.analyst_history.append({
                        "role": "analyst",
                        "content": f"Cortex Analyst 오류 (status: {resp.get('status')})",
                        "sql": None,
                        "data": None,
                    })
            except Exception as e:
                st.session_state.analyst_history.append({
                    "role": "analyst",
                    "content": f"오류가 발생했습니다: {str(e)[:150]}",
                    "sql": None,
                    "data": None,
                })
        st.experimental_rerun()

    if st.session_state.get("analyst_history"):
        if st.button("조회 초기화", key="reset_analyst"):
            st.session_state.analyst_history = []
            st.experimental_rerun()
