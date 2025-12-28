FROM python:3.11-slim

WORKDIR /app

# Sistem paketlerini kur
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Dosyaları kopyala
COPY requirements.txt .

# --- DÜZELTME BURADA: Başındaki # işaretlerini kaldırdık ---
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Kodları kopyala
COPY . .

EXPOSE 8000

# Sunucuyu başlat (Development modunda)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]