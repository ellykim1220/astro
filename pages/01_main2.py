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
