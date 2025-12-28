FROM python:3.11-slim

WORKDIR /app

# Sistem paketlerini kur (Bu lazım, yoksa pip install sırasında gcc hatası alırsın)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Dosyaları kopyala (requirements.txt içeri girsin ki sen kurabilesin)
COPY requirements.txt .
COPY . .

# --- BURASI ÖNEMLİ: Pip install'ı KAPATTIK ---
RUN pip install -r requirements.txt

EXPOSE 8000

# Konteyner kapanmasın diye sonsuz döngüde bekletiyoruz
CMD ["tail", "-f", "/dev/null"]