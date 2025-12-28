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
urlpatterns = [
    path('',include(router.urls)),
    path('hello/', views.HelloWorldView.as_view(), name='hello-world'),
	path('toplama/',views.ToplamaView.as_view(),name='toplama'),
	path('tahmin/',views.predict_irisView.as_view(),name='tahmin'),
	path('register/',views.RegisterView.as_view(),name='register'),    
	path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
