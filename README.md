# 📄 프로젝트 제안 보고서

>   **가상 IoT 센서 데이터 실시간 스트리밍 수집 및 저장**

------

## 1. 프로젝트 개요

본 프로젝트는 가상의 IoT 센서 데이터를 실시간으로 생성하여 Apache Kafka를 통해 스트리밍하고, 이를 소비하여 데이터베이스에 저장 및 시각화하는 **엔드 투 엔드(End-to-End) 데이터 파이프라인 구축**을 목표로 한다.
 이를 통해 데이터 엔지니어링 실무 핵심 역할인 **실시간 데이터 수집, 처리, 저장, 모니터링** 전 과정을 경험한다.

------

## 2. 프로젝트 목표

-   **가상의 IoT 센서 데이터 생성** 및 스트리밍 환경 구축
-   **Kafka Producer/Consumer** 구조 이해 및 구현
-   **InfluxDB(PostgreSQL 대체 가능)** 를 통한 데이터 저장
-   **Grafana**를 통한 실시간 데이터 시각화 대시보드 구축
-   **Airflow(선택)** 를 통한 데이터 흐름 관리 및 모니터링

------

## 3. 주제 선정 이유

| 항목                     | 설명                                                         |
| ------------------------ | ------------------------------------------------------------ |
| **손쉬운 데이터 생성**   | 실제 센서 없이 Python 스크립트를 통해 가짜 온도, 습도, 기압 등의 데이터를 랜덤 생성하여 쉽고 유연하게 프로젝트를 진행할 수 있다. |
| **Kafka 구조 심화 학습** | Producer가 데이터를 송신하고 Consumer가 데이터를 수신하는 Kafka의 스트리밍 모델을 명확하게 구현하고 이해할 수 있다. |
| **DB 저장 및 시각화**    | InfluxDB(또는 PostgreSQL)에 데이터를 저장하고 Grafana로 실시간 데이터 변화를 모니터링할 수 있어, 데이터 흐름과 저장 구조를 시각적으로 체득할 수 있다. |
| **확장성 확보**          | 센서 종류 추가, 이상치 탐지 기능 개발, 알림 시스템 추가 등 다양한 확장 프로젝트로 연결이 가능하다. 학습 깊이를 넓힐 수 있다. |

------

## 4. 프로젝트 시스템 구성도

```text
[ 가상 센서 데이터 생성기 (Python) ]
            ↓ (Kafka Producer)
         [ Kafka Topic ]
            ↓ (Kafka Consumer)
    [ InfluxDB or PostgreSQL (DB 저장) ]
            ↓
      [ Grafana 대시보드 (시각화) ]

```

-   Kafka Topic은 예를 들어 `sensor_data`로 설정
-   Consumer는 Kafka Topic에서 실시간으로 메시지를 수신하고 DB에 저장
-   Grafana는 InfluxDB를 데이터 소스로 연결하여 센서 데이터 시각화

------



## 5. 사용 기술 스택

| 분류                           | 기술 스택                  |
| ------------------------------ | -------------------------- |
| 프로그래밍                     | Python 3.x                 |
| 메시징 브로커                  | Apache Kafka               |
| 데이터베이스                   | InfluxDB (또는 PostgreSQL) |
| 데이터 시각화                  | Grafana                    |
| 파이프라인 관리 (선택)         | Apache Airflow             |
| 컨테이너 오케스트레이션 (옵션) | Docker-Compose             |

------

## 6. 세부 기능 및 확장성

| 기본 기능             | 상세 내용                                             |
| --------------------- | ----------------------------------------------------- |
| 가상 센서 데이터 생성 | 온도, 습도, 기압 등의 데이터 생성 (1초 또는 5초 간격) |
| Kafka Producer        | 센서 데이터를 Kafka Topic으로 실시간 송신             |
| Kafka Consumer        | Kafka Topic에서 데이터를 소비하고 DB에 저장           |
| InfluxDB 저장         | 센서 데이터를 시계열 데이터베이스에 삽입              |
| Grafana 대시보드      | 실시간 센서 데이터 시각화 대시보드 구축               |

| 확장 기능        | 상세 내용                                                    |
| ---------------- | ------------------------------------------------------------ |
| 센서 종류 추가   | 온도, 습도 외에 CO2, 미세먼지(PM2.5), 조도(LUX) 등 센서 추가 |
| 이상치 탐지 기능 | 정상 범위를 벗어난 센서 데이터 감지 및 경고                  |
| 알림 시스템      | 이상치 발생 시 Slack, Email 알림 발송                        |
| 데이터 집계      | 1분/5분/10분 평균값 집계 및 저장                             |
| 데이터 이력 분석 | 장기 데이터 저장 후 트렌드 분석 기능 추가                    |

------

## 7.디렉터리 구조 설계 예시

>   (프로젝트 이름: `iot-kafka-streaming-project`)

```bash
iot-kafka-streaming-project/
├── producer/                    # Kafka Producer (센서 데이터 생성 및 전송)
│   ├── producer.py
│   ├── sensor_generator.py      # 온도, 습도, 기압 랜덤 데이터 생성 로직
│   └── config.py                # Kafka 설정 정보
│
├── consumer/                    # Kafka Consumer (DB 저장용)
│   ├── consumer.py
│   ├── db_writer.py             # InfluxDB(PostgreSQL) 데이터 저장 모듈
│   └── config.py                # Kafka 및 DB 설정 정보
│
├── dags/                        # (선택) Airflow DAG 스크립트 (ETL 관리)
│   └── sensor_etl_dag.py
│
├── db/                          # DB 초기화 및 테이블 생성 스크립트
│   ├── init_influxdb.py
│   └── init_postgresql.sql
│
├── monitoring/                  # Grafana 대시보드 및 모니터링 설정
│   ├── grafana_dashboard.json   # 대시보드 템플릿
│   └── prometheus.yml           # (선택) Prometheus 설정
│
├── docker-compose.yml           # Kafka, Zookeeper, InfluxDB, Grafana 등 통합 실행
├── requirements.txt             # Python 의존성 관리
├── README.md                    # 프로젝트 소개 및 사용법 문서
└── .env                         # 환경 변수 (Kafka, DB 접속 정보 등)

```

**디렉터리 설계 핵심 포인트:**

-   Producer와 Consumer를 확실히 분리
-   DB 관련 스크립트 따로 관리
-   Grafana, Airflow 등 추가 모듈은 별도 디렉터리 관리
-   Docker-Compose로 전체 환경 통합 관리

## 8. 1개월 (4주) 완성 로드맵

### ✅ 0주차 (Day 0~2) - 프로젝트 준비

-    GitHub Repository 생성
-    디렉터리 구조 세팅 (`producer/`, `consumer/`, `db/`, `monitoring/`)
-    Docker-Compose 환경 구축 (Kafka, Zookeeper, InfluxDB, Grafana)

------

### ✅ 1주차 - **Kafka Producer/Consumer 구축**

-    `sensor_generator.py` 작성 (랜덤 온도, 습도, 기압 생성)
-    Kafka Producer(`producer.py`) 작성 (센서 데이터 발행)
-    Kafka Consumer(`consumer.py`) 작성 (Kafka에서 데이터 수신)
-    InfluxDB/PostgreSQL 테이블 설계 및 초기화 스크립트 작성
-    Consumer가 데이터를 DB에 저장하는 기능 구현 (`db_writer.py`)

**1주차 목표:**
 Kafka 스트림으로 가상 센서 데이터 생성 → Kafka Topic으로 전송 → 수신 → DB 저장까지 연결

------

### ✅ 2주차 - **Docker 통합 및 운영 환경 구축**

-    Kafka, Zookeeper, InfluxDB, Grafana를 하나의 `docker-compose.yml`로 통합
-    Python 애플리케이션(Producer/Consumer) Dockerfile 작성 및 컨테이너화
-    전체 서비스 `docker-compose up`으로 한 번에 구동
-    `.env` 파일로 환경 변수 분리 관리

**2주차 목표:**
 Kafka-DB-Grafana 통합 환경 완성 및 컨테이너 기반 운영 준비

------

### ✅ 3주차 - **Grafana 대시보드 구축 및 시각화**

-    Grafana 설치 및 InfluxDB 데이터 소스 연결
-    온도/습도/기압 실시간 그래프 대시보드 구성
-    기본적인 알림 트리거(Threshold) 설정 (ex: 온도 35도 이상 알림)
-    대시보드 템플릿(`grafana_dashboard.json`)으로 저장

**3주차 목표:**
 실시간 데이터 변화를 시각화하고, 이상 상황 알림 기능 기본 설정

------

### ✅ 4주차 - **고도화 및 확장 (옵션)**

-    센서 종류 추가 (ex: 미세먼지, CO2)
-    이상치 감지 로직 추가 (ex: 온도 급상승 시 Kafka에 알림 메시지 전송)
-    Airflow DAG 작성 (수집/저장 작업 스케줄링 및 모니터링)
-    프로젝트 최종 리팩토링 및 README 작성
-    추가: Grafana 알림을 Slack으로 연동

**4주차 목표:**
 확장성과 안정성 강화 + 프로젝트 문서화 및 최종 정리

### ✨ 요약

| 주차  | 주요 목표                                      |
| ----- | ---------------------------------------------- |
| 0주차 | 프로젝트 초기 세팅                             |
| 1주차 | Kafka Producer/Consumer 구현, 데이터 저장 연결 |
| 2주차 | Docker-Compose 통합 환경 구성                  |
| 3주차 | Grafana 실시간 시각화 및 대시보드 구축         |
| 4주차 | 이상치 감지/알림 확장 + 최종 프로젝트 마무리   |



## 9. 기대 효과

-   Kafka 기반 실시간 데이터 스트리밍 파이프라인 이해
-   Python을 활용한 Producer/Consumer 로직 구현 역량 강화
-   DB 설계 및 저장 성능 이해 (시계열 DB vs 관계형 DB)
-   데이터 시각화 및 모니터링 시스템 구축 경험
-   데이터 엔지니어 실무에 필요한 문제해결력과 확장 설계 경험

------

# ✨ 요약

| 항목        | 내용                                                         |
| ----------- | ------------------------------------------------------------ |
| 주제        | 가상 IoT 센서 데이터 실시간 스트리밍 수집 및 저장            |
| 주요 키워드 | Kafka, Python, InfluxDB, Grafana, 실시간 스트리밍, 데이터 파이프라인 |
| 선정 이유   | 쉽고 명확한 흐름, Kafka 구조 심화 학습, 저장 및 시각화까지 경험 가능, 높은 확장성 |
| 기대 성과   | 데이터 엔지니어링 실무 감각 체득 및 실시간 데이터 처리 시스템 구축 경험 |
