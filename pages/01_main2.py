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
