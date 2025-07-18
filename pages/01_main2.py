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



# streamlit_planet_info_app.py
import streamlit as st
from math import pi, sqrt

st.title("🌍 행성 정보 검색 및 생존 평가")
# 기준 안내
st.markdown("""
**평가 기준**

- **ΔP/P**: |자전 주기 - 공전 주기| / 공전 주기
  - **비동주기(생존 가능)**: ΔP/P ≥ 0.10
  - **동주기 우려**: ΔP/P < 0.10
- **대기 생존 (Hazard Index H)**:
  - O₂ 안전 범위: **19.5% ≤ O₂ ≤ 23.5%**
  - CO₂ 안전 상한: **CO₂ ≤ 0.5%**
  - 위험 지수 H = O₂ 위험도 + CO₂ 위험도
    - O₂ 위험도 = 0 (안전 범위) 또는 |O₂-21|/21
    - CO₂ 위험도 = 0 (≤0.5%) 또는 (CO₂-0.5)/0.5
  - **생존 가능**: H < 0.10
  - **생존 불가능**: H ≥ 0.10
"""
)

# ── 알려진 행성 데이터 사전 ──────────────────────────────────────
# rotation_days: 행성 자전 주기(일 단위), orbital_days: 공전 주기(일 단위)
PLANET_DATA = {
    'Mercury': {'rotation_days': 58.65,   'orbital_days': 87.97,  'O2': 0.0,  'CO2': 0.0},
    'Venus':   {'rotation_days': 243.02,  'orbital_days': 224.70, 'O2': 0.0,  'CO2': 96.5},
    'Earth':   {'rotation_days': 0.9973,  'orbital_days': 365.25, 'O2': 21.0, 'CO2': 0.04},
    'Mars':    {'rotation_days': 1.026,   'orbital_days': 687.0,  'O2': 0.13, 'CO2': 95.0},
    'Jupiter': {'rotation_days': 0.4137,  'orbital_days': 4331,   'O2': 0.0,  'CO2': 0.0},
    'Saturn':  {'rotation_days': 0.444,   'orbital_days': 10747,  'O2': 0.0,  'CO2': 0.0},
    'Uranus':  {'rotation_days': 0.718,   'orbital_days': 30589,  'O2': 0.0,  'CO2': 0.0},
    'Neptune': {'rotation_days': 0.671,   'orbital_days': 59800,  'O2': 0.0,  'CO2': 0.0}
}

# ── 평가 함수 ─────────────────────────────────────────────────────
SAFE_O2_MIN, SAFE_O2_MAX = 19.5, 23.5  # O₂ 안전 범위 (%)
SAFE_CO2_MAX = 0.5                     # CO₂ 안전 상한 (%)

def compute_delta_ratio(rot_days, orb_days):
    """ΔP/P 비율 = |P_spin - P_orb| / P_orb"""
    return abs(rot_days - orb_days) / orb_days


def compute_hazard(o2, co2):
    """대기 위험 지수 H 계산"""
    o2_r = 0 if SAFE_O2_MIN <= o2 <= SAFE_O2_MAX else abs(o2 - 21.0) / 21.0
    co2_r = 0 if co2 <= SAFE_CO2_MAX else (co2 - SAFE_CO2_MAX) / SAFE_CO2_MAX
    return o2_r + co2_r

# ── 사용자 인터페이스 ─────────────────────────────────────────────
planet = st.selectbox("행성 선택", options=list(PLANET_DATA.keys()))

info = PLANET_DATA.get(planet)
if info:
    st.write(f"### 선택된 행성: {planet}")
    st.write(f"- 자전 주기: {info['rotation_days']:.2f} 일")
    st.write(f"- 공전 주기: {info['orbital_days']:.2f} 일")
    st.write(f"- 대기 O₂: {info['O2']} %  ·  CO₂: {info['CO2']} %")

    # 동주기 여부
    delta_ratio = compute_delta_ratio(info['rotation_days'], info['orbital_days'])
    sync_msg = "❌ 동주기 우려" if delta_ratio < 0.10 else "✅ 비동주기 (생존 가능)"

    # 대기 생존 여부
    H = compute_hazard(info['O2'], info['CO2'])
    atm_msg = "✅ 생존 가능" if H < 0.10 else "❌ 생존 불가능"

    # 결과 출력
    st.write("---")
    st.write(f"**ΔP/P = {delta_ratio:.3f} → {sync_msg}**")
    st.write(f"**Hazard Index H = {H:.2f} → {atm_msg}**")
    st.caption(
        "ΔP/P 기준: ΔP/P ≥ 0.10 비동주기, "
        "대기 기준: O₂ 19.5–23.5%, CO₂ ≤ 0.5%"
    )
else:
    st.error("알 수 없는 행성입니다. 목록에서 선택하세요.")
