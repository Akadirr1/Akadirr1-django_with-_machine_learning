# Django Settings - Template ve Static Ayarları
# Bu ayarları Django projenizin settings.py dosyasına ekleyin

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Template ayarları
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # veya django_templates klasörünüzün yolu
        ],
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

# Static dosya ayarları
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media dosya ayarları (resimler için)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Login ayarları
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# Message framework için tag'ler
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}
