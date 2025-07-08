# file: exoplanet_life_check.py
import math

def calculate_luminosity(absolute_magnitude: float) -> float:
    return 10 ** ((4.83 - absolute_magnitude) / 2.5)

def calculate_habitable_zone(luminosity: float) -> tuple[float, float]:
    inner = 0.95 * math.sqrt(luminosity)
    outer = 1.37 * math.sqrt(luminosity)
    return inner, outer

def check_distance_in_habitable_zone(distance: float, inner: float, outer: float) -> bool:
    return inner <= distance <= outer

def evaluate_rotation_sync(mass: float) -> tuple[int, str]:
    # Hypothetical model for rotation difference (in days)
    rotation_difference = max(30 - mass * 5, 0)
    possibility = "불가능" if rotation_difference <= 7 else "가능"
    return rotation_difference, possibility

def evaluate_atmosphere(oxygen_percent: float, co2_percent: float) -> str:
    if oxygen_percent < 15 or oxygen_percent > 60:
        return "불가능"
    elif co2_percent >= 5:
        return "불가능"
    elif co2_percent >= 0.5:
        return "생존 가능성 매우 낮음"
    else:
        return "정상"

def run():
    print("[1] 항성의 절대 등급을 입력하세요:")
    abs_mag = float(input("절대 등급(M): "))

    luminosity = calculate_luminosity(abs_mag)
    inner, outer = calculate_habitable_zone(luminosity)
    print(f"광도: {luminosity:.2f} L☉")
    print(f"생명 가능 지대: {inner:.2f} AU ~ {outer:.2f} AU")

    distance = float(input("행성까지의 거리(AU): "))
    if check_distance_in_habitable_zone(distance, inner, outer):
        print("→ 생명 가능 지대 **내부**: 생명체 존재 가능")
    else:
        print("→ 생명 가능 지대 **외부**: 생명체 존재 불가능")

    print("\n[2] 항성의 질량을 입력하세요:")
    mass = float(input("항성 질량(M☉): "))
    rotation_diff, rotation_status = evaluate_rotation_sync(mass)
    print(f"항성-행성 자전 주기 차이: {rotation_diff:.1f}일 → {rotation_status}")

    print("\n[3] 행성 대기 조성 입력:")
    oxygen = float(input("산소 농도 (%): "))
    co2 = float(input("이산화탄소 농도 (%): "))
    atmosphere_status = evaluate_atmosphere(oxygen, co2)
    print(f"대기 평가 결과: {atmosphere_status}")

if __name__ == "__main__":
    run()
