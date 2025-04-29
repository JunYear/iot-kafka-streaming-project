import random
from datetime import datetime


def generate_sensor_data():
    """
    가상의 센서 데이터(온도, 습도, 기압, 미세먼지, 초미세먼지, co2농도)을 생성하는 함수,
    매 호출 시마다 새로운 랜덤 값을 반환한다.

    :return:
        dict: 센서 데이터 (timestamp, temperature, humidity, pressure, pm10, pm25, co2)
    """

    # 현재 UTC 기준 시간 생성 (글로벌 표준성 및 시간대 이슈 제거를 위해 UTC 설정)
    timestamp = datetime.utcnow().isoformat()

    # 온도(°C) 생성: 15°C ~ 30~ 범위
    temperature = round(random.uniform(15.0, 30.0), 2)

    # 습도(%) 생성: 30% ~ 90% 범위
    humidity = round(random.uniform(30.0, 90.0), 2)

    # 기압(hPa) 생성: 950hPa ~ 1050hPa 범위
    pressure = round(random.uniform(950.0, 1050), 2)

    # 미세먼지(μg/m³) 생성: 0μg/m³ ~ 150μg/m³ 범위
    pm10 = round(random.uniform(0.0, 150.0), 2)

    # 초미세먼지(μg/m³) 생성: 0μg/m³ ~ 100μg/m³ 범위
    pm25 = round(random.uniform(0.0, 100.0), 2)

    # 이산화탄소 농도(ppm) 생성: 400ppm ~ 1000ppm 범위
    co2 = round(random.uniform(400.0, 1000.0), 2)

    # 생성된 데이터들을 딕셔너리로 반환
    sensor_data = {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "pm10": pm10,
        "pm25": pm25,
        "co2": co2
    }

    return sensor_data


# 테스트 용도로 이 파일을 직접 실행했을 때 동작
if __name__ == "__main__":
    # 5회 출력해서 정상 작동 여부 확인
    for _ in range(5):
        data = generate_sensor_data()
        print(data)
