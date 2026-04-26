# Gunakan official Python 3.12 image yang ringan
FROM python:3.12-slim

# Set working directory di dalam container
WORKDIR /app

# Mencegah Python menulis file .pyc ke disk (menghemat ruang)
ENV PYTHONDONTWRITEBYTECODE=1
# Memastikan output Python langsung dikirim ke terminal tanpa di-buffer
ENV PYTHONUNBUFFERED=1

# Copy requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi
# Folder ./app di lokal di-copy ke folder /app/app di container
COPY ./app ./app

# Cloud Run mewajibkan aplikasi dengerin port dari variabel $PORT (default 8080)
# Baris EXPOSE di bawah ini lebih ke dokumentasi, karena Cloud Run akan me-override ini
EXPOSE 8080

# Perintah untuk menjalankan aplikasi
# Gunakan format Shell (tanpa kurung siku) agar variabel $PORT bisa terbaca oleh container
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}