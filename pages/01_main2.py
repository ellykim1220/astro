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










# streamlit_hr_dropdown_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from math import pi, sqrt

# 1. 주계열성 데이터
data = {
    'Spectral': ['O5','B0','A0','F0','G2','K5','M5'],
    'Mass':    [30.3,12.0,2.17,1.44,1.00,0.660,0.402],
    'Temp':    [54000,29200,9600,7350,5800,4400,3200],
    'Lum':     [846000,20000,22,4.3,1,0.19,0.026]
}
df = pd.DataFrame(data)

# 2. 계산 함수들
G = 6.67430e-11; M_SUN = 1.98847e30; AU = 1.495978707e11; DAY = 86400
P_SPIN = 24 * DAY

def orbital_period(a, m):
    return 2 * pi * sqrt((a*AU)**3 / (G * m * M_SUN))

def delta_p_ratio(a, m):
    P_orb = orbital_period(a, m)
    return abs(P_SPIN - P_orb) / P_orb

SAFE_O2_MIN, SAFE_O2_MAX = 19.5, 23.5
SAFE_CO2_MAX = 0.5
def hazard_index(o2, co2):
    o2_r = 0 if SAFE_O2_MIN<=o2<=SAFE_O2_MAX else abs(o2-21)/21
    c2_r = 0 if co2<=SAFE_CO2_MAX else (co2-SAFE_CO2_MAX)/SAFE_CO2_MAX
    return o2_r + c2_r

# 3. UI 구현
st.title("🌌 H–R 도 기반 생존성 평가 (드롭다운 방식)")
st.write("H–R 도는 시각화만 제공됩니다. 별 선택은 아래에서 해주세요.")

# 시각화만
fig = px.scatter(df, x='Temp', y='Lum', color='Spectral',
                 labels={'Temp':'온도 (K)', 'Lum':'광도 (L☉)'})
fig.update_layout(xaxis=dict(autorange='reversed'), yaxis_type='log')
st.plotly_chart(fig, use_container_width=True)

# 별 선택 기능
spec = st.selectbox("스펙트럴 타입 선택", df['Spectral'])
row = df[df['Spectral']==spec].iloc[0]
st.write(f"**선택된 별**: {spec}-type — M = {row.Mass:.2f} M☉, T = {row.Temp} K, L = {row.Lum:.2e} L☉")

# ΔP/P 계산
a = st.slider("궤도 반경 a (AU)", 0.01, 5.0, 1.0, 0.01)
ratio = delta_p_ratio(a, row.Mass)
st.write(f"**ΔP/P = {ratio:.3f}** — ",
         "✅ 비동주기 (생존 가능)" if ratio>=0.10 else "❌ 동주기 우려")

st.write("---")

# 대기 생존 평가
o2 = st.number_input("산소 농도 O₂ (%)", 0.0, 100.0, 21.0, 0.1)
co2 = st.number_input("이산화탄소 CO₂ (%)", 0.0, 10.0, 0.04, 0.01)
H = hazard_index(o2, co2)
st.write(f"**Hazard Index H = {H:.2f}** — ",
         "✅ 생존 가능" if H<0.10 else "❌ 생존 불가능")

st.caption("O₂ 19.5–23.5 %, CO₂ ≤ 0.5 %, 초기 자전 24 h 기준")

