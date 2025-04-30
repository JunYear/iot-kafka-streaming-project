# IoT Kafka Streaming Pipeline 🔗📡

>   실시간 IoT 센서 데이터를 Kafka로 수집하고, InfluxDB에 저장한 뒤 Grafana로 시각화하며,  Airflow를 통해 파이프라인을 주기적으로 모니터링하는 데이터 엔지니어링 프로젝트입니다.



![grafana_dashboard](monitoring/grafana_dashboard.png)

---

## 🛠️ 기술 스택

| 분야            | 도구                                  |
| --------------- | ------------------------------------- |
| 메시지 브로커   | Kafka, Zookeeper                      |
| 데이터 저장     | InfluxDB                              |
| 모니터링 시각화 | Grafana                               |
| 스케줄링/ETL    | Apache Airflow                        |
| 데이터 처리     | Python, kafka-python, influxdb-client |
| 컨테이너 관리   | Docker, Docker Compose                |

---

## 📁 프로젝트 구조

```bash
iot-kafka-streaming-project/
├── producer/                    # Kafka Producer (센서 데이터 생성 및 전송)
│   ├── producer.py
│   ├── sensor_generator.py
│   └── config.py
│
├── consumer/                    # Kafka Consumer (DB 저장용)
│   ├── consumer.py
│   ├── db_writer.py
│   └── config.py
│
├── common/                      # 공통 유틸리티 함수
│   └── anomaly_detector.py
│
├── dags/                        # Airflow DAG (ETL 관리)
│   └── sensor_etl_dag.py
│
├── db/                          # DB 초기화 스크립트
│   ├── init_influxdb.py
│   └── init_postgresql.sql
│
├── monitoring/                  # Grafana 대시보드 설정
│   ├── grafana_dashboard.json
│   └── prometheus.yml
│
├── .env                         # 환경 변수 설정
├── requirements.txt             # Python 패키지 목록
├── docker-compose.yml           # 통합 컨테이너 실행 설정
└── README.md                    # 프로젝트 설명 문서
```

## ⚙️ 실행 방법

1.  프로젝트 클론

```
git clone https://github.com/your-username/iot-kafka-streaming-project.git
cd iot-kafka-streaming-project
```

2.   의존성 설치

```
pip install -r requirements.txt
```

3.   Airflow 폴더 준비

```
mkdir -p airflow/dags airflow/logs airflow/plugins
cp dags/sensor_etl_dag.py airflow/dags/
```

4.   환경 변수 설정

`.env` 파일 예시:

```
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=sensor_data

INFLUXDB_URL=http://influxdb:8086
INFLUXDB_TOKEN=my-super-secret-token
INFLUXDB_ORG=my-org
INFLUXDB_BUCKET=sensor-bucket
```

5.   Docker Compose 실행

```
docker-compose up -d --build
```

6.   접속

| 서비스   | URL                   |
| -------- | --------------------- |
| Grafana  | http://localhost:3000 |
| Airflow  | http://localhost:8081 |
| InfluxDB | http://localhost:8086 |

------

## 📊 Grafana 대시보드 구성

-   온도, 습도, 기압
-   PM10 (미세먼지), PM2.5 (초미세먼지), CO2 농도
-   실시간 알림 트리거(Threshold 설정)

------

## 🔎 Airflow DAG 기능

-   Kafka/InfluxDB 연결 확인
-   Kafka 최신 메시지 기반 이상치 감지
-   DAG Task 실패 시 재시도/에러 추적 가능

------

## 🚨 이상치 감지 기준

| 항목  | 조건       |
| ----- | ---------- |
| 온도  | > 35°C     |
| 습도  | < 30%      |
| PM10  | > 80 μg/m³ |
| PM2.5 | > 50 μg/m³ |
| CO2   | > 900 ppm  |

------

## 📬 향후 확장 가능

-   Slack/Email 알림 연동
-   PostgreSQL 병행 저장
-   anomaly_events 별도 Measurement 저장
-   센서 수 추가 (초음파, 소음, 진동 등)

------

## 🧑‍💻 개발자

-   **이름**: jun Jeong
-   **이메일**: yyt1186@gmail.com
-   **기술블로그**: https://dysad.tistory.com