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

# Copy seluruh kode aplikasi (ingat, .env dan gcp-key.json akan di-skip karena .dockerignore)
COPY ./app ./app

# Expose port yang digunakan Uvicorn
EXPOSE 8000

# Perintah untuk menjalankan aplikasi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]