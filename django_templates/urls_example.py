# Django URL Configuration - Iris Sınıflandırma Sistemi
# Bu dosyayı Django projenizin urls.py dosyasına kopyalayın veya adapte edin

from django.urls import path
from . import views  # veya views_example

urlpatterns = [
    # Ana sayfa ve Auth
    path('', views.index, name='index'),
    path('login/', views.index, name='login'),  # index aynı zamanda login sayfası
    path('logout/', views.logout_view, name='logout'),
    path('kayit/', views.kayit, name='kayit'),
    
    # Iris CRUD
    path('iris/ekle/', views.iris_ekle, name='iris_ekle'),
    path('iris/listele/', views.iris_listele, name='iris_listele'),
    path('iris/guncelle/<int:id>/', views.iris_guncelle, name='iris_guncelle'),
    path('iris/sil/<int:id>/', views.iris_sil, name='iris_sil'),
    
    # Location CRUD
    path('lokasyon/ekle/', views.location_ekle, name='location_ekle'),
    path('lokasyon/listele/', views.location_listele, name='location_listele'),
    path('lokasyon/sil/<int:id>/', views.location_sil, name='location_sil'),
    
    # ML Tahmin
    path('tahmin/', views.tahmin, name='tahmin'),
]
