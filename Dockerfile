FROM python:3.11-slim

WORKDIR /app

# 1. Sistem paketlerini kur (ML ve Düzenleme için)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    nano \
    && rm -rf /var/lib/apt/lists/*

# 2. Gereksinim dosyasını kopyala ve kur
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 3. Proje dosyalarını kopyala
COPY . .

# 4. Portu dışarı aç
EXPOSE 8000

# 5. Migration yap ve sunucuyu başlat
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]