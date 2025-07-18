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
st.write("알려진 행성 이름을 선택하면 자전주기, 공전주기, 대기 조성 정보를 보여주고 생존 가능성을 평가합니다.")

# ── 알려진 행성 데이터 사전 ──────────────────────────────────────
# orbital_hr: 행성의 공전주기(시간 단위)
PLANET_DATA = {
    'Mercury': {'star_mass': 1.0, 'rotation_hr': 1407.5, 'orbital_hr': 87.97*24, 'O2': 0.0,  'CO2': 0.0},
    'Venus':   {'star_mass': 1.0, 'rotation_hr': 5832.5, 'orbital_hr': 224.7*24, 'O2': 0.0,  'CO2': 96.5},
    'Earth':   {'star_mass': 1.0, 'rotation_hr': 23.93,  'orbital_hr': 365.25*24, 'O2': 21.0, 'CO2': 0.04},
    'Mars':    {'star_mass': 1.0, 'rotation_hr': 24.62,  'orbital_hr': 687.0*24, 'O2': 0.13, 'CO2': 95.0},
    'Jupiter': {'star_mass': 1.0, 'rotation_hr': 9.93,   'orbital_hr': 4331*24,   'O2': 0.0,  'CO2': 0.0},
    'Saturn':  {'star_mass': 1.0, 'rotation_hr': 10.7,  'orbital_hr': 10747*24,  'O2': 0.0,  'CO2': 0.0},
    'Uranus':  {'star_mass': 1.0, 'rotation_hr': 17.2,  'orbital_hr': 30589*24,  'O2': 0.0,  'CO2': 0.0},
    'Neptune': {'star_mass': 1.0, 'rotation_hr': 16.1,  'orbital_hr': 59800*24,  'O2': 0.0,  'CO2': 0.0}
}

# ── 생존성 평가 함수 ────────────────────────────────────────────
SAFE_O2_MIN, SAFE_O2_MAX = 19.5, 23.5  # O₂ 안전 범위 (%)
SAFE_CO2_MAX = 0.5                     # CO₂ 안전 상한 (%)

def compute_delta_ratio(rotation_hr, orbital_hr):
    """ΔP/P 비율 = |P_spin - P_orb| / P_orb"""
    return abs(rotation_hr - orbital_hr) / orbital_hr


def compute_hazard(o2, co2):
    """대기 위험 지수 H 계산"""
    o2_r = 0 if SAFE_O2_MIN <= o2 <= SAFE_O2_MAX else abs(o2 - 21.0) / 21.0
    co2_r = 0 if co2 <= SAFE_CO2_MAX else (co2 - SAFE_CO2_MAX) / SAFE_CO2_MAX
    return o2_r + co2_r

# ── 사용자 인터페이스 ─────────────────────────────────────────────
planet = st.selectbox("행성 선택", options=list(PLANET_DATA.keys()))

# 선택된 행성 정보 로드
info = PLANET_DATA.get(planet)
if info:
    st.write(f"### 선택된 행성: {planet}")
    st.write(f"- 별 질량 M★: {info['star_mass']} M☉")
    st.write(f"- 자전 주기: {info['rotation_hr']:.2f} h")
    st.write(f"- 공전 주기: {info['orbital_hr']:.2f} h")
    st.write(f"- 대기 O₂: {info['O2']} %  ·  CO₂: {info['CO2']} %")

    # 동주기 여부 평가
    delta_ratio = compute_delta_ratio(info['rotation_hr'], info['orbital_hr'])
    sync_msg = "❌ 동주기 우려" if delta_ratio < 0.10 else "✅ 비동주기 (생존 가능)"

    # 대기 생존 여부 평가
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
