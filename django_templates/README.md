# Django 4.1 - Iris Sınıflandırma Sistemi Template'leri

Bu klasör, mevcut HTML/CSS/JS tabanlı projenin Django 4.1 template formatına dönüştürülmüş halini içerir.

## Dosya Yapısı

```
django_templates/
├── base.html              # Ana template (tüm sayfalar bu template'i extend eder)
├── index.html             # Ana sayfa ve login
├── kayit.html             # Kullanıcı kayıt sayfası
├── iris_ekle.html         # Yeni iris ekleme
├── iris_listele.html      # Iris listesi
├── iris_guncelle.html     # Iris güncelleme
├── iris_sil.html          # Iris silme onay
├── location_ekle.html     # Yeni lokasyon ekleme
├── location_listele.html  # Lokasyon listesi
├── location_sil.html      # Lokasyon silme onay
├── tahmin.html            # ML tahmin sayfası
├── views_example.py       # Örnek Django views
├── urls_example.py        # Örnek URL yapılandırması
├── models_example.py      # Örnek Django modelleri
├── forms_example.py       # Örnek Django formları
├── settings_example.py    # Örnek settings ayarları
└── README.md              # Bu dosya
```

## Django Projenize Entegrasyon

### 1. Template'leri Kopyalama

`django_templates/` içindeki `.html` dosyalarını Django projenizin `templates/` klasörüne kopyalayın:

```bash
cp django_templates/*.html /path/to/your/django_project/templates/
```

### 2. Settings.py Ayarları

`settings.py` dosyanıza şu ayarları ekleyin:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static dosyalar için
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### 3. Static Dosyalar

Çiçek resimlerini şu yapıda organize edin:

```
static/
└── images/
    ├── Iris_virginica.jpg
    ├── Iris_versicolor_3.jpg
    └── Kosaciec_szczecinkowaty_Iris_setosa.jpg
```

### 4. URL Yapılandırması

`urls.py` dosyanıza şu URL'leri ekleyin:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.index, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('kayit/', views.kayit, name='kayit'),
    path('iris/ekle/', views.iris_ekle, name='iris_ekle'),
    path('iris/listele/', views.iris_listele, name='iris_listele'),
    path('iris/guncelle/<int:id>/', views.iris_guncelle, name='iris_guncelle'),
    path('iris/sil/<int:id>/', views.iris_sil, name='iris_sil'),
    path('lokasyon/ekle/', views.location_ekle, name='location_ekle'),
    path('lokasyon/listele/', views.location_listele, name='location_listele'),
    path('lokasyon/sil/<int:id>/', views.location_sil, name='location_sil'),
    path('tahmin/', views.tahmin, name='tahmin'),
]
```

## Django Template Özellikleri

### Template Inheritance

Tüm sayfalar `base.html` template'ini extend eder:

```html
{% extends 'base.html' %}

{% block title %}Sayfa Başlığı{% endblock %}

{% block content %}
    <!-- Sayfa içeriği -->
{% endblock %}
```

### Static Dosyalar

```html
{% load static %}
<img src="{% static 'images/Iris_virginica.jpg' %}" alt="Iris">
```

### URL Oluşturma

```html
<a href="{% url 'iris_listele' %}">Iris Listele</a>
<a href="{% url 'iris_guncelle' record.id %}">Güncelle</a>
```

### CSRF Token

Tüm POST formlarında CSRF token gereklidir:

```html
<form method="post">
    {% csrf_token %}
    <!-- form alanları -->
</form>
```

### Koşullu Gösterim

```html
{% if user.is_authenticated %}
    <p>Hoşgeldin {{ user.username }}</p>
{% else %}
    <p>Lütfen giriş yapın</p>
{% endif %}
```

### Döngüler

```html
{% for record in records %}
    <tr>
        <td>{{ record.id }}</td>
        <td>{{ record.species }}</td>
    </tr>
{% empty %}
    <tr><td colspan="2">Kayıt bulunamadı</td></tr>
{% endfor %}
```

### Mesajlar

```html
{% if messages %}
    {% for message in messages %}
        <div class="message {{ message.tags }}">{{ message }}</div>
    {% endfor %}
{% endif %}
```

## Gereksinimler

- Django >= 4.1
- Python >= 3.8

## Notlar

- CSS stilleri `base.html` içinde inline olarak tanımlanmıştır
- İsterseniz CSS'i ayrı bir static dosyaya taşıyabilirsiniz
- Örnek view, model ve form dosyaları projenize göre düzenlenmelidir
