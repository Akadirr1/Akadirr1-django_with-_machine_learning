from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('hello/', views.HelloWorldView.as_view(), name='hello-world'),
	path('toplama',views.ToplamaView.as_view(),name='toplama'),
	path('tahmin',views.predict_irisView.as_view(),name='tahmin'),
	path('register',views.RegisterView.as_view(),name='register'),    
	path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
