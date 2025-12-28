FROM python:3.11-slim
WORKDIR /app

# Sistem paketlerini kur
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Dosyaları kopyala
COPY requirements.txt .
COPY . .

# DİKKAT: pip install komutunu YORUMA ALDIM (# koydum)
# RUN pip install -r requirements.txt

# Şimdilik sunucu başlatmasın, sadece "uyumasın" yeter
CMD ["tail", "-f", "/dev/null"]