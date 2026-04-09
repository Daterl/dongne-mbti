"""
동네 MBTI — 서울 동네의 성격을 찾아서
Streamlit in Snowflake App
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session


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
               EI_SCORE, SN_SCORE, TF_SCORE, JP_SCORE
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
.mbti-card {
    border-radius: 16px;
    padding: 24px;
    color: white;
    text-align: center;
    margin-bottom: 16px;
}
.mbti-type {
    font-size: 56px;
    font-weight: 900;
    letter-spacing: 6px;
    margin: 0;
}
.mbti-subtitle {
    font-size: 15px;
    opacity: 0.85;
    margin-top: 6px;
}
.character-summary {
    font-size: 17px;
    font-style: italic;
    background: rgba(255,255,255,0.15);
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 14px;
}
.axis-chip {
    display: inline-block;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px;
    background: rgba(255,255,255,0.2);
}
.section-title {
    font-size: 18px;
    font-weight: 700;
    color: #333;
    margin: 16px 0 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ── 헤더 ─────────────────────────────────────────────────────────────────────
st.markdown("# 🏙️ 동네 MBTI")
st.markdown("##### 서울 동네의 성격을 데이터로 읽다 — 서초 · 영등포 · 중구 118개 동")

# ── 탭 ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏠 동네 카드", "💬 동네 찾기", "📊 이사 예보"])

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
        st.markdown(f"""
        <div class="mbti-card" style="background: linear-gradient(135deg, {color}, {color}cc);">
            <p class="mbti-type">{mbti}</p>
            <p class="mbti-subtitle">{selected_gu} {selected_dong}</p>
            <div>
                <span class="axis-chip">{ei}</span>
                <span class="axis-chip">{sn}</span>
                <span class="axis-chip">{tf}</span>
                <span class="axis-chip">{jp}</span>
            </div>
            <div class="character-summary">"{row['CHARACTER_SUMMARY']}"</div>
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
        st.plotly_chart(fig, use_container_width=True)

        # 4축 수치 메트릭
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("E/I", f"{row['EI_SCORE']:+.2f}", help="양수=외향(E), 음수=내향(I)")
        c2.metric("S/N", f"{row['SN_SCORE']:+.2f}", help="양수=실용(S), 음수=문화(N)")
        c3.metric("T/F", f"{row['TF_SCORE']:+.2f}", help="양수=이성/부유(T), 음수=감성/서민(F)")
        c4.metric("J/P", f"{row['JP_SCORE']:+.2f}", help="양수=변화(P), 음수=안정(J)")

    # ── 동네 비교 ──
    st.divider()
    st.markdown("### 🔍 다른 동네와 비교")

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
        st.plotly_chart(fig2, use_container_width=True)

        # 궁합 점수 (축별 거리 기반)
        distance = sum(abs(row[a] - c_row[a]) for a in axes)
        compatibility = max(0, int(100 - distance * 12))
        st.metric(
            f"🤝 {selected_dong} × {c_dong} 궁합 점수",
            f"{compatibility}점",
            help="4축 z-score 거리 기반. 100점에 가까울수록 성격이 유사한 동네.",
        )

# ════════════════════════════════════════════════════════════════════════════
# 탭 2: 자연어 동네 찾기 (Cortex Agent — Search + Analyst 오케스트레이션)
# ════════════════════════════════════════════════════════════════════════════
import _snowflake
import json as _json

def _run_agent(history: list) -> str:
    """Cortex Agent REST 호출 → 텍스트 응답 추출."""
    try:
        resp = _snowflake.send_snow_api_request(
            "POST",
            "/api/v2/cortex/agent:run",
            {},
            {},
            {
                "agent": "DONGNE_MBTI.PUBLIC.DONGNE_AGENT",
                "messages": history,
                "experimental": {},
            },
            None,
            30000,
        )
        if resp.get("status") != 200:
            return f"⚠️ Agent 오류 (status: {resp.get('status', 'unknown')})"

        parts = []
        for line in resp.get("content", "").split("\n"):
            if not line.startswith("data:"):
                continue
            try:
                data = _json.loads(line[5:].strip())
                if data.get("object") == "message.delta":
                    for item in data.get("delta", {}).get("content", []):
                        if item.get("type") == "text":
                            parts.append(item.get("text", ""))
            except Exception:
                pass
        return "".join(parts) or "응답을 받지 못했습니다."
    except Exception as e:
        return f"⚠️ 오류: {str(e)[:200]}"


with tab2:
    st.markdown("### 💬 자연어로 동네 찾기")
    st.caption("Cortex Agent (Search + Analyst) — 서초·영등포·중구 118개 동")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent_history" not in st.session_state:
        st.session_state.agent_history = []

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
                st.rerun()

    # ── 대화 히스토리 출력 ──
    for msg in st.session_state.messages:
        icon = "🧑" if msg["role"] == "user" else "🤖"
        st.markdown(f"**{icon}** {msg['content']}")
        st.divider()

    # ── 채팅 입력 (st.chat_input 미지원 SiS 버전 호환) ──
    prompt = st.session_state.pop("_pending", None)
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        text_in = st.text_input(
            "질문 입력",
            placeholder="예: 서초구에서 조용하고 부유한 동네 추천해줘",
            label_visibility="collapsed",
            key="chat_text_input",
        )
    with col_btn:
        send = st.button("전송", use_container_width=True)

    if send and text_in:
        prompt = text_in

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.container():
            st.markdown(prompt)

        st.session_state.agent_history.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        })

        with st.spinner("동네를 찾고 있어요..."):
            answer_text = _run_agent(st.session_state.agent_history)
        st.markdown(f"**🤖** {answer_text}")
        st.divider()

        st.session_state.agent_history.append({
            "role": "assistant",
            "content": [{"type": "text", "text": answer_text}],
        })
        st.session_state.messages.append({"role": "assistant", "content": answer_text})

    if st.session_state.messages:
        if st.button("대화 초기화", key="reset_chat"):
            st.session_state.messages = []
            st.session_state.agent_history = []
            st.rerun()

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
        price_df["YYYYMMDD"] = pd.to_datetime(price_df["YYYYMMDD"].astype(str))
        price_df = price_df.sort_values("YYYYMMDD")

        # ML 예측 데이터 로드
        forecast_df = load_forecast(t3_gu, t3_dong)
        has_forecast = not forecast_df.empty

        if has_forecast:
            forecast_df["TS"] = pd.to_datetime(forecast_df["TS"])

        # ── 통합 시세 차트 (실적 + ML 예측) ──
        fig3 = go.Figure()

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
            # 예측 신뢰구간 (밴드)
            fig3.add_trace(go.Scatter(
                x=pd.concat([forecast_df["TS"], forecast_df["TS"][::-1]]),
                y=pd.concat([forecast_df["UPPER_BOUND"], forecast_df["LOWER_BOUND"][::-1]]),
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
            title=f"{t3_gu} {t3_dong} 아파트 매매 평당가 추이 {'+ ML 예측' if has_forecast else ''}",
            xaxis_title="월",
            yaxis_title="평당가 (만원)",
            hovermode="x unified",
            height=400,
            margin=dict(t=50, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig3, use_container_width=True)

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
                            'auto',
                            '{forecast_prompt.replace("'", "''")}'
                        ) AS FORECAST
                    """).collect()[0]["FORECAST"]

                    st.markdown("#### 🏡 AI 이사 전망")
                    st.info(forecast)
                except Exception as e:
                    st.error(f"전망 생성 중 오류가 발생했습니다: {str(e)[:100]}")
