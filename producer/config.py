import os
from dotenv import load_dotenv

# .env 파일을 읽어와 환경 변수 설정
load_dotenv()

# Kafka 서버 정보와 토픽 이름을 환경 변수에서 불러오기
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "host.docker.internal:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_data")