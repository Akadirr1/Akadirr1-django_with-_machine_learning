from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import HelloSerializer
from .serializers import ToplamaSerializers
from .serializers import IrisInputSerializer
from .serializers import RegisterSerializers
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
import os
import joblib
import numpy as np
from django.conf import settings

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
            s_len=serializer.validated_data['sepal_length']
            s_wid=serializer.validated_data['sepal_width']
            p_len=serializer.validated_data['petal_length']
            p_wid=serializer.validated_data['petal_width']
            tahmin="setosa"
            return Response({
            "mesaj": "Veriler alındı, model çalışmaya hazır!",
            "girilen_degerler": serializer.validated_data,
            "tahmin": tahmin
        })
        return Response(serializer.errors,status=400)
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