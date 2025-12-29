from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router=DefaultRouter()
router.register(r'records',views.IrisCrudViewSet,basename='iris-records')
router.register(r'locations',views.LocationViewSet,basename='location-records')

# API URL'leri
api_urlpatterns = [
    path('',include(router.urls)),
    path('hello/', views.HelloWorldView.as_view(), name='hello-world'),
	path('toplama/',views.ToplamaView.as_view(),name='toplama'),
	path('tahmin/',views.predict_irisView.as_view(),name='tahmin'),
	path('register/',views.RegisterView.as_view(),name='register'),    
	path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Web Template URL'leri
web_urlpatterns = [
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
    path('tahmin-web/', views.tahmin_web, name='tahmin_web'),
]

urlpatterns = api_urlpatterns
