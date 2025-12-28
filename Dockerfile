FROM python:3.10-slim

WORKDIR /app

# 1. Sanal ortamı (venv) oluştur
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
# Sanal ortamı PATH'e ekle (Böylece 'source activate' demeye gerek kalmaz)
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Derleme araçlarını kur (Gereksiz ama garanti olsun)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Önce requirements kopyala ve kur
COPY requirements.txt .
RUN pip install --upgrade pip
# Artık pip, yukarıdaki PATH ayarı sayesinde otomatik olarak venv içine kuracak
RUN pip install -r requirements.txt

# 3. Kalan dosyaları kopyala
COPY . .

EXPOSE 8000

# Venv aktif olduğu için direkt komutu yazabiliriz
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]