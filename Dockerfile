FROM python:3.10-slim

WORKDIR /app

# Sistem kütüphanelerini kur (ML kütüphaneleri için şart)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Requirements dosyasını kopyala ve kur
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Kodları kopyala
COPY . .

# Portu aç
EXPOSE 8000

# DİREKT DEVELOPMENT SUNUCUSUNU BAŞLAT
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]