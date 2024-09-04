FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py /app/

ENV PYTHONUNBUFFERED=1

# 서버 실행
CMD ["python", "app.py"]
