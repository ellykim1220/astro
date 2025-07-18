# streamlit_deltaP_orbital.py
import streamlit as st
from math import pi, sqrt

# 물리 상수
G = 6.67430e-11               # 중력 상수 (m³ kg⁻¹ s⁻²)
M_SUN = 1.98847e30           # 태양 질량 (kg)
AU = 1.495978707e11          # 천문단위 (m)
DAY_SEC = 86400              # 하루 (초)

# 지구형 초기 자전주기 가정: 24 시간
P_SPIN_INIT_SEC = 24 * DAY_SEC

def orbital_period_sec(a_au: float, m_star_solar: float) -> float:
    """
    케플러 제3법칙으로 공전주기 계산:
    P = 2π sqrt(a³ / G M_star)
    """ 
    a = a_au * AU
    M = m_star_solar * M_SUN
    return 2 * pi * sqrt(a**3 / (G * M))

def delta_p_ratio(a_au: float, m_star_solar: float) -> float:
    """
    ΔP/P = |P_spin_init - P_orb| / P_orb
    """
    P_orb = orbital_period_sec(a_au, m_star_solar)
    return abs(P_SPIN_INIT_SEC - P_orb) / P_orb

def classify_ratio(ratio: float) -> str:
    """10 % 기준으로 동주기 여부 판단"""
    return "✅ 충분한 차이 — 비동주기 (생존 가능)" if ratio >= 0.10 else "❌ 거의 동주기 (생존 불가능)"

# Streamlit UI 구성
st.title("🌌 ΔP/P 계산기 (공전‑자전 주기 차이)")
st.write("항성 질량(M☉)과 행성–항성 거리(AU)을 입력하면 ΔP/P를 계산해 비동주기 여부를 판단합니다.")

m_star = st.number_input("항성 질량 M★ (태양질량‑단위)", min_value=0.01, max_value=10.0, value=1.0, step=0.01)
a = st.number_input("궤도 반경 a (AU)", min_value=0.001, max_value=100.0, value=1.0, step=0.01)

if st.button("계산 🔄"):
    ratio = delta_p_ratio(a, m_star)
    st.write(f"**ΔP/P = {ratio:.3f}**")
    st.write("")  # 한 줄 띄우기
    st.write(f"### {classify_ratio(ratio)}")

# streamlit_app.py
import streamlit as st

# 상수 설정
SAFE_O2_MIN = 19.5
SAFE_O2_MAX = 23.5
SAFE_CO2_MAX = 0.5
THRESHOLD_H = 0.10

def hazard_index(o2_pct: float, co2_pct: float) -> float:
    if SAFE_O2_MIN <= o2_pct <= SAFE_O2_MAX:
        o2_risk = 0.0
    else:
        o2_risk = abs(o2_pct - 21.0) / 21.0
    if co2_pct <= SAFE_CO2_MAX:
        co2_risk = 0.0
    else:
        co2_risk = (co2_pct - SAFE_CO2_MAX) / SAFE_CO2_MAX
    return o2_risk + co2_risk

def classify_survival(H: float) -> str:
    return "✅ 생존 가능" if H < THRESHOLD_H else "❌ 생존 불가능"

# UI 구성
st.title("🌍 대기 생존 가능성 평가기")
st.write("산소(O₂)와 이산화탄소(CO₂) 농도를 입력하면 생존 가능성을 계산합니다.")

o2 = st.number_input("산소 농도 O₂ (% v/v)", min_value=0.0, max_value=100.0, value=21.0, step=0.1)
co2 = st.number_input("이산화탄소 농도 CO₂ (% v/v)", min_value=0.0, max_value=100.0, value=0.04, step=0.01)

if st.button("결과 확인"):
    H = hazard_index(o2, co2)
    st.write(f"**Hazard Index H = {H:.2f}**")
    st.write("")  # 한 줄 띄우기
    st.write(f"### {classify_survival(H)}")

# streamlit_hr_deltaP.py
import streamlit as st
from math import pi, sqrt

# — 기존 ΔP/P 계산 로직 —
G = 6.67430e-11
M_SUN = 1.98847e30
AU = 1.495978707e11
DAY_SEC = 86400
P_SPIN_INIT_SEC = 24 * DAY_SEC

def orbital_period_sec(a_au: float, m_star_solar: float) -> float:
    return 2 * pi * sqrt((a_au * AU)**3 / (G * m_star_solar * M_SUN))

def delta_p_ratio(a_au: float, m_star_solar: float) -> float:
    P_orb = orbital_period_sec(a_au, m_star_solar)
    return abs(P_SPIN_INIT_SEC - P_orb) / P_orb

def classify_ratio(ratio: float) -> str:
    return "✅ 충분한 차이 — 비동주기 (생존 가능)" if ratio >= 0.10 else "❌ 거의 동주기 (생존 불가능)"



# streamlit_hr_interactive.py
import streamlit as st
import pandas as pd
import plotly.express as px
from math import pi, sqrt

# 📊 스펙트럴 타입별 주요 정보 (대표값)
data = {
    'Spectral': ['O5','B0','A0','F0','G2','K5','M5'],
    'Mass': [30.3, 18.0, 3.2, 1.7, 1.0, 0.69, 0.15],  # M☉  :contentReference[oaicite:2]{index=2}
    'Temp': [54000, 30000, 9600, 7500, 5780, 4410, 3120],  # 표면 온도 (K)
    'Lum': [846000, 20000, 80, 6, 1, 0.16, 0.0027]  # 광도 (L☉)
}
df = pd.DataFrame(data)

# ΔP/P 계산 함수
G = 6.67430e-11; M_SUN = 1.98847e30; AU = 1.495978707e11; DAY = 86400
P_SPIN = 24 * DAY

def orbital_period(a_au, m_solar):
    return 2 * pi * sqrt((a_au*AU)**3 / (G * m_solar * M_SUN))

def delta_p_ratio(a, m_solar):
    P_orb = orbital_period(a, m_solar)
    return abs(P_SPIN - P_orb) / P_orb

# UI
st.title("🌟 H–R 다이어그램 기반 ΔP/P 계산기")
st.write("주계열상의 별 중 하나를 클릭하여 궤도 반경에 따른 ΔP/P 및 생존판정을 확인하세요.")

fig = px.scatter(df, x='Temp', y='Lum', color='Spectral', hover_data=['Mass'],
                 labels={'Temp':'Temperature (K)', 'Lum':'Luminosity (L☉)'},
                 title="Click a star type")
fig.update_layout(xaxis=dict(autorange='reversed'), yaxis_type='log')
hr = st.plotly_chart(fig, use_container_width=True)

# 클릭 이벤트 처리 (requires streamlit-plotly-events component)
from streamlit_plotly_events import plotly_events
pts = plotly_events(fig, click_event=True, hover_event=False)

if pts:
    idx = pts[0]['pointIndex']
    row = df.iloc[idx]
    st.write(f"**선택한 별: {row.Spectral}-type**")
    st.write(f"- 질량 = {row.Mass:.2f} M☉  ·  표면 온도 = {row.Temp} K  ·  광도 = {row.Lum:.2e} L☉")
    a = st.slider("🚀 궤도 반경 a (AU)", 0.01, 10.0, 1.0, 0.01)
    ratio = delta_p_ratio(a, row.Mass)
    st.write(f"\n**ΔP/P = {ratio:.3f}**")
    verdict = "✅ 생존 가능 (비동주기)" if ratio >= 0.10 else "❌ 동주기 우려"
    st.write(f"### {verdict}")
    st.caption("ΔP/P 계산식은 초기 자전주기를 24 h로 가정하고, ΔP/P ≥ 0.1이면 비동주기로 간주합니다.")
