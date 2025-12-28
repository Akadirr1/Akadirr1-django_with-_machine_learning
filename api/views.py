from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import HelloSerializer
from .serializers import ToplamaSerializers
from .serializers import IrisInputSerializer
from .serializers import RegisterSerializers
from .serializers import IrisDataSerializers
from .serializers import LocationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import IrisData
from .models import Location
import os
import joblib
import numpy as np
from django.conf import settings
from .ml_loader import LOADED_MODELS
class HelloWorldView(APIView):
    """
    A simple Hello World API endpoint.
    """

    @extend_schema(
        responses={200: HelloSerializer},
        description="Returns a hello world message"
    )
    def get(self, request):
        """
        Return a hello world message.
        """
        data = {"message": "Hello, World! Django 4.1 + DRF + Scalar is working!"}
        return Response(data, status=status.HTTP_200_OK)
class ToplamaView(APIView):
	
    @extend_schema(
            parameters=[ToplamaSerializers],#scalarda direkt kullanıcı girmesi gereken parametreleri görsün diye dotnette otomatik oluyordu burda elle
            responses=ToplamaSerializers#bu dönüş için ama pek işlevi yok şuanda
	)
    def get(self,request):
        serializer = ToplamaSerializers(data=request.query_params)
        if serializer.is_valid():
            s1=serializer.validated_data['sayi1']
            s2=serializer.validated_data['sayi2']
            return Response({"sonuc":s1+s2})
        return Response(serializer.errors,status=400)   
class predict_irisView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=IrisInputSerializer,
	)
    def post(self,request):
        serializer=IrisInputSerializer(data=request.data)
        if serializer.is_valid():
            data =serializer.validated_data
            ISIMLER = {
                    0: "Setosa",
                    1: "Versicolor", 
                    2: "Virginica"
                }
            secilen_tip=data['model_type']
            model = LOADED_MODELS.get(secilen_tip)
            if not model:
                return response({"bu model şuanda devredışı"},status=500)
            
            input_vector=np.array([[
                data['sepal_length'],
                data['sepal_width'],
                data['petal_length'],
                data['petal_width']
            ]])
            try:
                predict = model.predict(input_vector)[0]
                if(predict==0):
                    isim ="Setosa"
                elif(predict==1):
                    isim ="Versicolor"
                elif(predict==2):
                    isim ="Versicolor"
                return Response(isim,status=200)
            except Exception as e:
                return Response({"hata": f"Tahmin sırasında hata: {str(e)}"}, status=500)
        print("❌ VALIDATION HATASI:", serializer.errors)
        return Response(serializer.errors,status=400)
class IrisCrudViewSet(viewsets.ModelViewSet):
    serializer_class=IrisDataSerializers
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return IrisData.objects.filter(owner=self.request.user).order_by('-created_at')
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
class RegisterView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]
    @extend_schema(
        request=RegisterSerializers
	)
    def post(self,request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mesaj": "Kral hoşgeldin, kayıt başarılı!"}, 
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=400)
class LocationViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=LocationSerializer
    queryset=Location.objects.all()