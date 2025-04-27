from kafka import KafkaProducer
import json
import time
import os
from sensor_generator import generate_sensor_data
from dotenv import load_dotenv

# .env 파일을 읽어와 환경 변수 설정
load_dotenv()

# Kafka 서버 정보와 토픽 이름을 환경 변수에서 불러오기
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "host.docker.internal:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_data")

# KafkaProducer 인스턴스 생성
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # 데이터를 JSON 형태로 직렬화
)

def send_sensor_data():
    """
    가상의 센서 데이터를 생성하여 Kafka 토픽으로 전송하는 함수.
    """

    # 1개의 센서 데이터 생성
    sensor_data = generate_sensor_data()

    # Kafka 토픽으로 데이터 전송
    producer.send(KAFKA_TOPIC, value=sensor_data)

    # 전송 로그 출력 (개발 편의용)
    print(f"[Kafka Producer] Sent data: {sensor_data}")

if __name__ == "__main__":
    # 무한 루프로 주기적으로 데이터 전송
    try:
        while True:
            send_sensor_data()
            time.sleep(5)  # 5초마다 데이터 전송
    except KeyboardInterrupt:
        print("Producer stopped manually.")
    finally:
        # 프로듀서 종료
        producer.close()
