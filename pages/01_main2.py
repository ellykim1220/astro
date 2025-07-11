import math

def calculate_luminosity(Mv):
    """절대 등급(Mv)으로부터 광도(L/L_sun)를 계산"""
    Mv_sun = 4.83  # 태양의 절대 등급
    L_over_L_sun = 10 ** (0.4 * (Mv_sun - Mv))
    return L_over_L_sun

def calculate_habitable_zone(L_over_L_sun):
    """광도로부터 생명가능지대의 내/외부 경계 계산 (단위: AU)"""
    r_inner = math.sqrt(L_over_L_sun)  # 내측 경계
    r_outer = math.sqrt(L_over_L_sun * 4)  # 외측 경계
    return r_inner, r_outer

def main():
    try:
        # 사용자로부터 절대 등급 입력
        Mv = float(input("항성의 절대 등급(Mv)을 입력하세요: "))
        
        # 광도 계산
        L = calculate_luminosity(Mv)
        
        # 생명가능지대 계산
        r_inner, r_outer = calculate_habitable_zone(L)
        
        # 결과 출력
        print(f"\n항성의 광도: {L:.2f} L_⊙")
        print(f"생명가능지대 내측 경계: {r_inner:.2f} AU")
        print(f"생명가능지대 외측 경계: {r_outer:.2f} AU")
        
    except ValueError:
        print("유효한 숫자를 입력하세요.")

if __name__ == "__main__":
    main()
