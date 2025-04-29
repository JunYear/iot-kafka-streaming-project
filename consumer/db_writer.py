from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv

#.env 파일 로드
load_dotenv()

# InfluxDB 접속 정보 환경변수에서 불러오기
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

# InfluxDB 클라이언트 생성
client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)

# Write API (데이터 쓰기 전용)
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_sensor_data_to_influxdb(sensor_data: dict):
    """
    센서 데이터를 InfluxDB에 저장하는 함수.

    Args:
        sensor_data (dict): 센서 데이터 (timestamp, temperacture, humidity, pressure, pm10, pm25, co2)
    """

    # InfluxDB에 저장할 포인트 데이터 생성
    point = (
        Point("sensor_measurements")    # Measurement 이름 (ex: 테이블 비슷한 개념)
        .tag("device", "virtual_sensor_01")      # 태그: 기기 식별자
        .field("temperature", sensor_data["temperature"])   # 필드: 온도 값
        .field("humidity", sensor_data["humidity"])         # 필드: 습도 값
        .field("pressure", sensor_data["pressure"])         # 필드: 기압 값
        .field("pm10", sensor_data["pm10"])                 # 필드: 미세먼지 값
        .field("pm25", sensor_data["pm25"])                 # 필드: 초미세먼지 값
        .field("co2", sensor_data["co2"])                   # 필드: co2 농도 값
        .time(sensor_data["timestamp"], WritePrecision.NS)  # 시간: 초 단위로 저장
    )

    # 데이터 쓰기 (버킷 지정)
    write_api.write(
        bucket=INFLUXDB_BUCKET,
        org=INFLUXDB_ORG,
        record=point
    )

    # 저장 성공 로그
    print(f"[InfluxDB] Data written: {sensor_data}")

if __name__ == "__main__":
    # 테스트용 코드
    test_data = {
        "timestamp": "2024-04-27T06:30:00Z",
        "temperature": 23.5,
        "humidity": 45.2,
        "pressure": 1012.3,
        "pm10": 30.0,
        "pm25": 15.0,
        "co2": 500.0
    }
    write_sensor_data_to_influxdb(test_data)
