# consumer/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# 실행 파일 및 requirements 복사
COPY consumer.py db_writer.py ./
COPY requirements.txt ./

# 공통 모듈 복사
COPY ../common ./common

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "consumer.py"]
