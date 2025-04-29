import os
import json
from kafka import KafkaConsumer
from dotenv import load_dotenv
from db_writer import write_sensor_data_to_influxdb
from common.anomaly_detector import detect_anomalies

# .env 파일을 읽어와 환경 변수 설정
load_dotenv()

# Kafka 서버 정보와 토픽 이름을 환경 변수에서 불러오기
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_data")

# KafkaConsumer 인스턴스 생성
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',  # 가장 처음 메시지부터 읽기
    enable_auto_commit=True,       # 메시지를 처음 읽은 후 자동으로 오프셋 커밋
    group_id='sensor-data-consumer-group',  # Consumer Group ID 설정
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # 메시지를 JSON 디코딩
)

def consume_sensor_data():
    """
    Kafka 토픽에서 실시간으로 센서 데이터를 읽고,
    이상치 감지 후 InfluxDB에 저장하는 함수.
    """

    print("[Kafka Consumer] Listening for messages...")

    for message in consumer:
        # message.value는 JSON 디코딩된 Python dict 객체
        sensor_data = message.value

        # 수신한 데이터 출력
        print(f"[Kafka Consumer] Received data: {sensor_data}")

        # 이상치 감지
        alerts = detect_anomalies(sensor_data)
        if alerts:
            for alert in alerts:
                print(f"[ALERT DETECTED] {alert}")

        # Kafka에서 받은 센서 데이터를 InfluxDB에 저장
        write_sensor_data_to_influxdb(sensor_data)

if __name__ == "__main__":
    try:
        consume_sensor_data()
    except KeyboardInterrupt:
        print("Consumer stopped manually.")
    finally:
        # Consumer는 특별한 close 호출 없이 안전하게 종료됨
        pass
