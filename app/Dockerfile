# Python 이미지 기반으로 도커 환경 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY gcp.py /app/
COPY server.py /app/
COPY service_key.json /app/

# 서버 실행
CMD ["python", "server.py"]
