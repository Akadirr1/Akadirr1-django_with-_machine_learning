# 1. Python'un resmi sürümünü kullan (ML kütüphaneleri için slim yerine normal sürüm daha güvenli olabilir ama slim de denenebilir)
FROM python:3.10-slim

# 2. Konteyner içindeki çalışma dizinini ayarla
WORKDIR /app

# 3. Python'un .pyc dosyaları oluşturmasını ve çıktıları tamponlamasını engelle (Logları anlık görmek için)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. İşletim sistemi bağımlılıklarını kur (ML kütüphaneleri bazen gcc vb. ister)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libopenblas-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*
# 5. Gereksinimleri kopyala ve kur
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. Proje dosyalarını kopyala
COPY . /app/

# 7. Portu dışarı aç
EXPOSE 8000

# 8. Sunucuyu başlat (Development için runserver)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]