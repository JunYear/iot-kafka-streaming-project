import os
import json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient
from common.anomaly_detector import detect_anomalies

# DAG 기본 설정
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='sensor_etl_dag',
    default_args=default_args,
    description='Kafka → InfluxDB ETL + 이상치 감지 파이프라인',
    schedule_interval='*/1 * * * *',  # 매 1분마다 실행
    start_date=datetime(2025, 4, 28),
    catchup=False,
    tags=['sensor', 'etl', 'kafka', 'influxdb', 'anomaly']
) as dag:

    def check_kafka_topic():
        """Kafka 연결 확인"""
        KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
        KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_data")

        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='sensor-etl-monitor-group',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        print("[Airflow] Kafka 연결 성공: 토픽 정상 수신")
        consumer.close()

    def check_influxdb_connection():
        """InfluxDB 연결 확인"""
        INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
        INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "my-super-secret-token")
        INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")

        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        health = client.health()

        if health.status != "pass":
            raise Exception("[Airflow] InfluxDB 연결 실패")
        print("[Airflow] InfluxDB 연결 성공")
        client.close()

    def detect_anomalies_from_kafka():
        """Kafka에서 최신 데이터 가져와서 이상치 감지"""
        KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
        KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_data")

        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='sensor-anomaly-detector-group',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            consumer_timeout_ms=5000  # 5초 동안 메시지 없으면 종료
        )

        anomalies_detected = False

        for message in consumer:
            sensor_data = message.value
            alerts = detect_anomalies(sensor_data)

            if alerts:
                anomalies_detected = True
                for alert in alerts:
                    print(f"[ALERT DETECTED] {alert}")

        if not anomalies_detected:
            print("[Airflow] 최근 데이터에 이상치 없음")

        consumer.close()

    # Task 1: Kafka 연결 체크
    task_check_kafka = PythonOperator(
        task_id='check_kafka_topic',
        python_callable=check_kafka_topic
    )

    # Task 2: InfluxDB 연결 체크
    task_check_influxdb = PythonOperator(
        task_id='check_influxdb_connection',
        python_callable=check_influxdb_connection
    )

    # Task 3: Kafka 데이터 이상치 감지
    task_detect_anomalies = PythonOperator(
        task_id='detect_anomalies_from_kafka',
        python_callable=detect_anomalies_from_kafka
    )

    # 실행 순서 정의
    task_check_kafka >> task_check_influxdb >> task_detect_anomalies
