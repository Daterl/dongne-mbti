"""
동네 MBTI — 서울 동네의 성격을 찾아서
Streamlit in Snowflake App
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session
from animals import MBTI_ANIMALS, MBTI_ANIMAL_NAMES

# ── AI 모델 설정 ──────────────────────────────────────────────────────────────
# 모델명을 상수로 분리 → 업그레이드 시 여기만 변경
MODEL_PRIMARY = "mistral-large2"      # 주 모델: 고성능 자연어 응답
MODEL_FALLBACK = "snowflake-arctic"   # 폴백 모델: Primary 실패 시


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

# ── 탭 ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🏠 동네 카드", "💬 동네 찾기", "📊 이사 예보", "🔬 데이터 탐색"])

# ════════════════════════════════════════════════════════════════════════════
# 탭 1: 동네 MBTI 카드
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    profiles_df = load_profiles()

    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        gu_list = sorted(profiles_df["SGG"].unique())
        selected_gu = st.selectbox("구 선택", gu_list)
    with col_sel2:
        dong_list = sorted(profiles_df[profiles_df["SGG"] == selected_gu]["EMD"].unique())
        selected_dong = st.selectbox("동 선택", dong_list)

    row = profiles_df[
        (profiles_df["SGG"] == selected_gu) & (profiles_df["EMD"] == selected_dong)
    ]

    if row.empty:
        st.warning("해당 동의 데이터가 없습니다.")
        st.stop()

    row = row.iloc[0]
    mbti = row["MBTI"]
    color = MBTI_COLORS.get(mbti, "#555")

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

# ════════════════════════════════════════════════════════════════════════════
# 탭 2: 자연어 동네 찾기 (Cortex Search + AI_COMPLETE)
# ════════════════════════════════════════════════════════════════════════════
import _snowflake
import json as _json
import re as _re

_SUPPORTED_SGG = {"서초구", "영등포구", "중구"}


def _check_unsupported_district(query: str):
    """지원 범위 외 구 언급 감지 → 안내 메시지 반환, 없으면 None."""
    found = _re.findall(r'\S+구', query)
    unsupported = [s for s in found if s not in _SUPPORTED_SGG]
    if unsupported:
        names = "·".join(unsupported)
        return (
            f"죄송해요! **{names}**는 현재 서비스 범위에 없어요. "
            f"동네 MBTI는 **서초구·영등포구·중구** 3개 구만 지원합니다. "
            f"이 중 하나로 다시 질문해 주세요! 😊"
        )
    return None


def _extract_sgg(query: str):
    """쿼리에서 구 이름 감지."""
    for sgg in _SUPPORTED_SGG:
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
    """Cortex Search → AI_COMPLETE(mistral-large2) 멀티턴 대화 답변 생성."""
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
            SELECT SNOWFLAKE.CORTEX.COMPLETE(
                '{MODEL_PRIMARY}',
                ARRAY_CONSTRUCT({messages_sql})
            )
        """).collect()[0][0]
    except Exception as e:
        # Primary 실패 시 Fallback 모델로 재시도 (히스토리 없이 단순 호출)
        try:
            fallback_prompt = f"{system_msg}\n\n{current_user_msg}".replace("'", "''")
            answer = session.sql(
                f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{MODEL_FALLBACK}', '{fallback_prompt}')"
            ).collect()[0][0]
        except Exception as e2:
            answer = f"응답 생성 오류: {str(e2)[:100]}"

    return answer, results


with tab2:
    st.markdown("### 💬 자연어로 동네 찾기")
    st.caption("🔍 Cortex Search (하이브리드 벡터+키워드 검색) + AI_COMPLETE — 서초·영등포·중구 118개 동")
    st.info(
        "**작동 방식**: 질문 → Snowflake Cortex Search로 관련 동네 프로필 검색 → "
        f"AI({MODEL_PRIMARY})가 검색 결과를 바탕으로 맞춤 답변 생성",
        icon="🤖",
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
        icon = "🧑" if msg["role"] == "user" else "🤖"
        st.markdown(f"**{icon}** {msg['content']}")
        st.divider()

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

# ════════════════════════════════════════════════════════════════════════════
# 탭 3: 이사 예보 (ML FORECAST + AI 분석)
# ════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=3600)
def load_forecast(sgg: str, emd: str):
    """PRICE_FORECAST_RESULT에서 ML 예측값 로드 (Issue #16)."""
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

with tab3:
    st.markdown("### 📊 이사 예보 — 시세 트렌드 & ML 예측")

    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        t3_gu = st.selectbox("구 선택 ", sorted(load_mbti_result()["SGG"].unique()), key="t3_gu")
    with col_t2:
        t3_dong_list = sorted(load_mbti_result()[load_mbti_result()["SGG"] == t3_gu]["EMD"].unique())
        t3_dong = st.selectbox("동 선택 ", t3_dong_list, key="t3_dong")

    price_df = load_price_history(t3_gu, t3_dong)

    if price_df.empty:
        st.info(f"📭 {t3_gu} {t3_dong}의 아파트 실거래가 데이터가 없습니다.")
    else:
        price_df["YYYYMMDD"] = pd.to_datetime(price_df["YYYYMMDD"].astype(str), errors="coerce")
        price_df = price_df.dropna(subset=["YYYYMMDD"]).sort_values("YYYYMMDD")

        # ML 예측 데이터 로드
        forecast_df = load_forecast(t3_gu, t3_dong)
        has_forecast = not forecast_df.empty

        if has_forecast:
            forecast_df["TS"] = pd.to_datetime(forecast_df["TS"])
            forecast_df["FORECAST_PRICE"] = pd.to_numeric(forecast_df["FORECAST_PRICE"], errors="coerce")
            forecast_df["LOWER_BOUND"] = pd.to_numeric(forecast_df["LOWER_BOUND"], errors="coerce").fillna(forecast_df["FORECAST_PRICE"])
            forecast_df["UPPER_BOUND"] = pd.to_numeric(forecast_df["UPPER_BOUND"], errors="coerce").fillna(forecast_df["FORECAST_PRICE"])

        # ── 통합 시세 차트 (실적 + ML 예측) ──
        fig3 = go.Figure()

        # Y축 범위: 데이터 범위에 맞게 설정 (0부터 시작하지 않음)
        y_min = price_df["AVG_PRICE"].min() * 0.90
        y_max = price_df["AVG_PRICE"].max() * 1.10

        # 실적 데이터
        fig3.add_trace(go.Scatter(
            x=price_df["YYYYMMDD"],
            y=price_df["AVG_PRICE"],
            mode="lines+markers",
            line=dict(color="#2874A6", width=2),
            marker=dict(size=4),
            name="실거래 평당가",
        ))

        if has_forecast:
            if not forecast_df["UPPER_BOUND"].isna().all():
                y_max = max(y_max, forecast_df["UPPER_BOUND"].max() * 1.05)
            # 예측 신뢰구간 (밴드)
            fig3.add_trace(go.Scatter(
                x=list(forecast_df["TS"]) + list(forecast_df["TS"][::-1]),
                y=list(forecast_df["UPPER_BOUND"]) + list(forecast_df["LOWER_BOUND"][::-1]),
                fill="toself",
                fillcolor="rgba(231,76,60,0.15)",
                line=dict(color="rgba(0,0,0,0)"),
                name="예측 범위 (90%)",
                hoverinfo="skip",
            ))
            # 예측 중앙값
            fig3.add_trace(go.Scatter(
                x=forecast_df["TS"],
                y=forecast_df["FORECAST_PRICE"],
                mode="lines+markers",
                line=dict(color="#E74C3C", width=2, dash="dash"),
                marker=dict(size=6, symbol="diamond"),
                name="ML 예측",
            ))

        fig3.update_layout(
            xaxis_title="월",
            yaxis_title="평당가 (만원)",
            yaxis=dict(range=[y_min, y_max]),
            hovermode="x unified",
            height=420,
            margin=dict(t=20, b=40, l=60, r=20),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
            ),
        )
        st.plotly_chart(fig3, use_container_width=True, config={"staticPlot": True})

        # ── 메트릭 ──
        if len(price_df) >= 2:
            latest = price_df.iloc[-1]["AVG_PRICE"]
            prev = price_df.iloc[-2]["AVG_PRICE"]
            delta = latest - prev
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("최근 평당가", f"{latest:,.0f}만원", f"{delta:+,.0f}만원")
            m2.metric("기간", f"{price_df['YYYYMMDD'].iloc[0].strftime('%Y.%m')} ~ {price_df['YYYYMMDD'].iloc[-1].strftime('%Y.%m')}")
            m3.metric("데이터", f"{len(price_df)}개월")
            if has_forecast:
                pred_latest = forecast_df.iloc[-1]["FORECAST_PRICE"]
                pred_delta = pred_latest - latest
                m4.metric("3개월 후 예측", f"{pred_latest:,.0f}만원", f"{pred_delta:+,.0f}만원")

        # ── AI 이사 전망 ──
        st.divider()
        if st.button("🤖 AI 이사 전망 생성", key="forecast_btn"):
            with st.spinner("AI가 시세를 분석하고 있어요..."):
                try:
                    recent_prices = price_df.tail(6)["AVG_PRICE"].tolist()
                    ml_info = ""
                    if has_forecast:
                        pred_vals = forecast_df["FORECAST_PRICE"].tolist()
                        ml_info = f" ML 예측 향후 {len(pred_vals)}개월: {[round(v) for v in pred_vals]}만원."
                    forecast_prompt = (
                        f"{t3_gu} {t3_dong} 최근 6개월 아파트 매매 평당가: {[round(p) for p in recent_prices]}만원."
                        f"{ml_info} 이 데이터를 바탕으로 향후 이사 타이밍에 대한 짧고 솔직한 전망을 2-3문장으로 알려줘. "
                        f"트렌드 방향과 이사 적합성을 판단해줘."
                    )
                    forecast = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.COMPLETE(
                            '{MODEL_PRIMARY}',
                            '{forecast_prompt.replace("'", "''")}'
                        ) AS FORECAST
                    """).collect()[0]["FORECAST"]

                    st.markdown("#### 🏡 AI 이사 전망")
                    st.info(forecast)
                except Exception as e:
                    st.error(f"전망 생성 중 오류가 발생했습니다: {str(e)[:100]}")

# ════════════════════════════════════════════════════════════════════════════
# 탭 4: 데이터 탐색 — Cortex Analyst (NL2SQL)
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 🔬 Cortex Analyst — 자연어로 MBTI 데이터 조회")
    st.caption(
        "Snowflake Cortex Analyst가 자연어 질문을 SQL로 자동 변환하여 정형 데이터를 조회합니다. "
        "Cortex Search(비정형 텍스트 검색)와 달리, 점수·통계·순위 등 수치 데이터 질의에 최적화."
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
        ex_cols = st.columns(len(_ANALYST_EXAMPLES))
        for i, ex in enumerate(_ANALYST_EXAMPLES):
            if ex_cols[i].button(ex, key=f"analyst_ex_{i}", use_container_width=True):
                st.session_state["_analyst_pending"] = ex
                st.experimental_rerun()

    # 대화 히스토리 출력
    for msg in st.session_state.get("analyst_history", []):
        icon = "🧑" if msg["role"] == "user" else "📊"
        st.markdown(f"**{icon}** {msg['content']}")
        if msg.get("sql"):
            with st.expander("생성된 SQL 보기"):
                st.code(msg["sql"], language="sql")
        if msg.get("data") is not None:
            st.dataframe(msg["data"], use_container_width=True)
        st.divider()

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
