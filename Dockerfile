# Gunakan official Python 3.12 image yang ringan
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Perintah format Shell murni (tanpa tanda kutip JSON)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}