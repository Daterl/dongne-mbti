"""
동네 MBTI — 서울 동네의 성격을 찾아서
Streamlit in Snowflake App
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from snowflake.snowpark.context import get_active_session

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
            fillcolor=color + "55",
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
            fillcolor=color + "44",
            line=dict(color=color, width=2),
            name=f"{selected_dong} ({mbti})",
        ))
        # 비교 동
        fig2.add_trace(go.Scatterpolar(
            r=[max(0, min(1, (c_row[a] + 3) / 6)) for a in axes] + [max(0, min(1, (c_row[axes[0]] + 3) / 6))],
            theta=labels + [labels[0]],
            fill="toself",
            fillcolor=c_color + "44",
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
# 탭 2: 자연어 동네 찾기 (Cortex Agent)
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 💬 자연어로 동네 찾기")
    st.caption("Cortex Search + Cortex Analyst + Cortex Agent 기반")

    # 대화 히스토리 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 대화 출력
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "data" in msg and msg["data"] is not None:
                st.dataframe(msg["data"], use_container_width=True)

    # 사용자 입력
    if prompt := st.chat_input("예: 서초구에서 조용하고 가족 친화적인 동네 추천해줘"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("동네를 찾고 있어요..."):
                try:
                    # Cortex Agent 호출 (Issue #12 완료 후 활성화)
                    result = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.COMPLETE(
                            'mistral-large2',
                            ARRAY_CONSTRUCT(
                                OBJECT_CONSTRUCT('role', 'system', 'content',
                                    '당신은 서울 동네 MBTI 전문가입니다. 서초구, 영등포구, 중구의 118개 동에 대해 답변합니다.
                                     각 동네는 MBTI 성격 유형이 있으며, 사용자 질문에 맞는 동네를 추천하세요.'),
                                OBJECT_CONSTRUCT('role', 'user', 'content', '{prompt.replace("'", "''")}')
                            )
                        ) AS ANSWER
                    """).collect()[0]["ANSWER"]

                    # 관련 동네 데이터 검색
                    search_result = session.sql(f"""
                        SELECT SGG, EMD, MBTI, CHARACTER_SUMMARY
                        FROM DONGNE_MBTI.PUBLIC.DONG_PROFILES
                        WHERE PROFILE_TEXT ILIKE '%{prompt[:20].replace("'", "''")}%'
                           OR CHARACTER_SUMMARY ILIKE '%조용%'
                        LIMIT 5
                    """).to_pandas()

                    st.markdown(result)
                    if not search_result.empty:
                        st.dataframe(search_result, use_container_width=True)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result,
                        "data": search_result if not search_result.empty else None,
                    })

                except Exception as e:
                    msg = f"⚠️ 잠시 오류가 발생했습니다. 다시 시도해주세요. ({str(e)[:80]})"
                    st.error(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg})

    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# 탭 3: 이사 예보
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 📊 이사 예보 — 시세 트렌드 & AI 전망")

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

        # 시세 트렌드 차트
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=price_df["YYYYMMDD"],
            y=price_df["AVG_PRICE"],
            mode="lines+markers",
            line=dict(color="#2874A6", width=2),
            marker=dict(size=4),
            name="매매 평당가",
        ))
        fig3.update_layout(
            title=f"{t3_gu} {t3_dong} 아파트 매매 평당가 추이",
            xaxis_title="월",
            yaxis_title="평당가 (만원)",
            hovermode="x unified",
            height=380,
            margin=dict(t=50, b=40),
        )
        st.plotly_chart(fig3, use_container_width=True)

        # 최근 변화 메트릭
        if len(price_df) >= 2:
            latest = price_df.iloc[-1]["AVG_PRICE"]
            prev = price_df.iloc[-2]["AVG_PRICE"]
            delta = latest - prev
            m1, m2, m3 = st.columns(3)
            m1.metric("최근 평당가", f"{latest:,.0f}만원", f"{delta:+,.0f}만원")
            m2.metric("기간", f"{price_df['YYYYMMDD'].iloc[0].strftime('%Y.%m')} ~ {price_df['YYYYMMDD'].iloc[-1].strftime('%Y.%m')}")
            m3.metric("데이터 포인트", f"{len(price_df)}개월")

        # AI 이사 전망
        st.divider()
        if st.button("🤖 AI 이사 전망 생성", key="forecast_btn"):
            with st.spinner("AI가 시세를 분석하고 있어요..."):
                try:
                    recent_prices = price_df.tail(6)["AVG_PRICE"].tolist()
                    forecast_prompt = f"""
                    {t3_gu} {t3_dong} 최근 6개월 아파트 매매 평당가: {recent_prices}만원
                    이 데이터를 바탕으로 향후 이사 타이밍에 대한 짧고 솔직한 전망을 2-3문장으로 알려줘.
                    숫자보다는 트렌드 방향과 이사 적합성을 판단해줘.
                    """
                    forecast = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.COMPLETE(
                            'mistral-large2',
                            '{forecast_prompt.strip().replace("'", "''")}'
                        ) AS FORECAST
                    """).collect()[0]["FORECAST"]

                    st.markdown("#### 🏡 AI 이사 전망")
                    st.info(forecast)
                except Exception as e:
                    st.error(f"전망 생성 중 오류가 발생했습니다: {str(e)[:100]}")
