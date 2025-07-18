# streamlit_full_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from math import pi, sqrt

# — 1. 주계열성 데이터 정의 —
data = {
    'Spectral': ['O5','B0','A0','F0','G2','K5','M5'],
    'Mass':    [30.3, 12.0,   2.17, 1.44, 1.00, 0.660, 0.402],  # M☉ :contentReference[oaicite:4]{index=4}
    'Temp':    [54000,29200,9600,7350,5800,4400,3200],           # K
    'Lum':     [846000,20000,22,4.3,1,0.19,0.026]                # L☉
}
df = pd.DataFrame(data)

# — 2. ΔP/P 계산 함수 —
G = 6.67430e-11
M_SUN = 1.98847e30
AU = 1.495978707e11
DAY = 86400
P_SPIN = 24 * DAY

def orbital_period(a_au, m_solar):
    return 2 * pi * sqrt((a_au*AU)**3 / (G * m_solar * M_SUN))

def delta_p_ratio(a, m_solar):
    P_orb = orbital_period(a, m_solar)
    return abs(P_SPIN - P_orb) / P_orb

# — 3. 대기 생존 함수 —
SAFE_O2_MIN, SAFE_O2_MAX = 19.5, 23.5
SAFE_CO2_MAX = 0.5
def hazard_index(o2_pct, co2_pct):
    o2_risk = 0 if SAFE_O2_MIN <= o2_pct <= SAFE_O2_MAX else abs(o2_pct - 21.0)/21.0
    co2_risk = 0 if co2_pct <= SAFE_CO2_MAX else (co2_pct - SAFE_CO2_MAX)/SAFE_CO2_MAX
    return o2_risk + co2_risk

# — 4. UI 시작 —
st.title("🌌 통합 앱: H–R 도 + ΔP/P + 대기 생존 평가")
st.write("H–R 도에서 별을 클릭하면 ΔP/P와 대기 생존 여부를 함께 볼 수 있어요.")

# — 5. H–R 도 시각화 및 클릭 —
fig = px.scatter(df, x='Temp', y='Lum', color='Spectral',
                 hover_data=['Mass'], labels={'Temp':'온도 (K)', 'Lum':'광도 (L☉)'})
fig.update_layout(xaxis=dict(title='온도 (왼→뜨거움)', autorange='reversed'),
                  yaxis_title='광도 (로그 스케일)', yaxis_type="log")
st.write("### 🌟 H–R 도 (주계열성)")
from streamlit_plotly_events import plotly_events
pts = plotly_events(fig, click_event=True, hover_event=False)
st.plotly_chart(fig, use_container_width=True)

if pts:
    row = df.iloc[pts[0]['pointIndex']]
    st.write(f"#### 선택한 별: **{row.Spectral}-type**")
    st.write(f"- 질량: {row.Mass:.2f} M☉ · 온도: {row.Temp} K · 광도: {row.Lum:.2e} L☉")

    # — 6. ΔP/P 계산 UI —
    a = st.slider("궤도 반경 a (AU)", 0.01, 5.0, 1.0, 0.01)
    ratio = delta_p_ratio(a, row.Mass)
    result_dyn = "✅ 비동주기 (생존 가능)" if ratio >= 0.10 else "❌ 동주기 우려"
    st.write(f"\n**ΔP/P = {ratio:.3f} → {result_dyn}**")

    # — 7. 대기 생존 입력 UI —
    o2 = st.number_input("산소 농도 O₂ (% v/v)", min_value=0.0, max_value=100.0, value=21.0, step=0.1)
    co2 = st.number_input("이산화탄소 CO₂ (% v/v)", min_value=0.0, max_value=10.0, value=0.04, step=0.01)
    H = hazard_index(o2, co2)
    result_atm = "✅ 생존 가능" if H < 0.10 else "❌ 생존 불가능"
    st.write(f"**Hazard Index H = {H:.2f} → {result_atm}**")

    st.caption("ΔP/P는 초기 자전 24 h 가정, 대기 평가는 O₂(19.5–23.5 %), CO₂ ≤ 0.5 % 기준입니다.")

