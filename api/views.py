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
from .models import CustomUser
import os
import joblib
import numpy as np
from django.conf import settings
from .ml_loader import LOADED_MODELS
import csv
from django.utils.encoding import smart_str
from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication
# Django Template Views için import'lar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .forms import UserRegistrationForm, IrisForm, LocationForm, TahminForm
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


# ==========================================
# Django Template Based Views (Web Arayüzü)
# ==========================================

def index(request):
    """Ana sayfa ve login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)  # Browser kapanınca session biter
            messages.success(request, 'Giriş başarılı!')
            return redirect('index')
        else:
            return render(request, 'index.html', {'error': 'Kullanıcı adı veya şifre hatalı!'})
    
    return render(request, 'index.html')


def logout_view(request):
    """Çıkış view"""
    logout(request)
    messages.info(request, 'Başarıyla çıkış yaptınız.')
    return redirect('index')


def kayit(request):
    """Kullanıcı kayıt view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
            return redirect('index')
        else:
            return render(request, 'kayit.html', {'form': form, 'error': 'Kayıt sırasında hata oluştu.'})
    
    return render(request, 'kayit.html', {'form': UserRegistrationForm()})


@csrf_exempt
@require_POST
def ajax_tahmin(request):
    """AJAX ile tahmin yapan endpoint"""
    try:
        data = json.loads(request.body)
        ml_model = data.get('ml_model', 'knn')
        sepal_length = float(data.get('sepal_length', 0))
        sepal_width = float(data.get('sepal_width', 0))
        petal_length = float(data.get('petal_length', 0))
        petal_width = float(data.get('petal_width', 0))
        
        species_names = {
            0: "Iris-setosa",
            1: "Iris-versicolor", 
            2: "Iris-virginica"
        }
        
        model = LOADED_MODELS.get(ml_model)
        if not model:
            return JsonResponse({'error': 'Model bulunamadı'}, status=400)
        
        input_vector = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        predict_result = model.predict(input_vector)[0]
        prediction = species_names.get(predict_result, "Bilinmeyen")
        
        return JsonResponse({'success': True, 'prediction': prediction})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='login')
def iris_ekle(request):
    """Yeni Iris ekleme view"""
    locations = Location.objects.all()
    
    if request.method == 'POST':
        form = IrisForm(request.POST)
        if form.is_valid():
            iris = form.save(commit=False)
            iris.owner = request.user
            iris.save()
            messages.success(request, 'Iris örneği başarıyla eklendi!')
            return redirect('iris_listele')
        else:
            return render(request, 'iris_ekle.html', {
                'locations': locations,
                'form': form,
                'error': 'Form bilgilerini kontrol edin.'
            })
    
    return render(request, 'iris_ekle.html', {
        'locations': locations,
        'form': IrisForm()
    })


@login_required(login_url='login')
def iris_listele(request):
    """Iris kayıtlarını listeleme view"""
    records = IrisData.objects.filter(owner=request.user).order_by('-created_at')
    
    return render(request, 'iris_listele.html', {
        'records': records,
    })


@login_required(login_url='login')
def iris_guncelle(request, id):
    """Iris güncelleme view"""
    record = get_object_or_404(IrisData, id=id, owner=request.user)
    
    if request.method == 'POST':
        record.sepal_length = float(request.POST.get('sepal_length'))
        record.sepal_width = float(request.POST.get('sepal_width'))
        record.petal_length = float(request.POST.get('petal_length'))
        record.petal_width = float(request.POST.get('petal_width'))
        record.species = request.POST.get('species')
        record.save()
        messages.success(request, 'Iris örneği başarıyla güncellendi!')
        return redirect('iris_listele')
    
    return render(request, 'iris_guncelle.html', {
        'record': record,
    })


@login_required(login_url='login')
def iris_sil(request, id):
    """Iris silme view"""
    record = get_object_or_404(IrisData, id=id, owner=request.user)
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Iris örneği başarıyla silindi!')
        return redirect('iris_listele')
    
    return render(request, 'iris_sil.html', {
        'record': record,
    })


@login_required(login_url='login')
def location_ekle(request):
    """Yeni lokasyon ekleme view"""
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lokasyon başarıyla eklendi!')
            return redirect('location_listele')
        else:
            return render(request, 'location_ekle.html', {
                'form': form,
                'error': 'Form bilgilerini kontrol edin.'
            })
    
    return render(request, 'location_ekle.html', {'form': LocationForm()})


@login_required(login_url='login')
def location_listele(request):
    """Lokasyonları listeleme view"""
    locations = Location.objects.all()
    
    return render(request, 'location_listele.html', {
        'locations': locations,
    })


@login_required(login_url='login')
def location_sil(request, id):
    """Lokasyon silme view"""
    location = get_object_or_404(Location, id=id)
    
    if request.method == 'POST':
        location.delete()
        messages.success(request, 'Lokasyon başarıyla silindi!')
        return redirect('location_listele')
    
    return render(request, 'location_sil.html', {
        'location': location,
    })


@login_required(login_url='login')
def iris_csv(request):
    """CSV Import/Export view"""
    return render(request, 'iris_csv.html')


@login_required(login_url='login')
def tahmin_web(request):
    """ML Tahmin view (Web Arayüzü)"""
    prediction = None
    model_name = None
    form = TahminForm()
    
    model_names = {
        'knn': 'K-En Yakın Komşu (KNN)',
        'svm': 'Destek Vektör Makinesi (SVM)',
        'decision_tree': 'Karar Ağacı Sınıflandırıcı'
    }
    
    species_names = {
        0: "Iris-setosa",
        1: "Iris-versicolor", 
        2: "Iris-virginica"
    }
    
    if request.method == 'POST':
        form = TahminForm(request.POST)
        if form.is_valid():
            ml_model = form.cleaned_data['ml_model']
            sepal_length = form.cleaned_data['sepal_length']
            sepal_width = form.cleaned_data['sepal_width']
            petal_length = form.cleaned_data['petal_length']
            petal_width = form.cleaned_data['petal_width']
            
            # ML Model ile tahmin yap
            model = LOADED_MODELS.get(ml_model)
            if model:
                input_vector = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
                try:
                    predict_result = model.predict(input_vector)[0]
                    prediction = species_names.get(predict_result, f"Bilinmeyen ({predict_result})")
                    model_name = model_names.get(ml_model, ml_model)
                except Exception as e:
                    return render(request, 'tahmin.html', {
                        'form': form,
                        'error': f'Tahmin sırasında hata: {str(e)}'
                    })
            else:
                return render(request, 'tahmin.html', {
                    'form': form,
                    'error': 'Seçilen model şu anda kullanılamıyor.'
                })
    
    return render(request, 'tahmin.html', {
        'form': form,
        'prediction': prediction,
        'model_name': model_name,
    })
class IrisCSVExportView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="iris_verileri.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width', 'Species', 'Location ID'])
        
        # Kullanıcıya ait verileri çekiyorum burda
        records = IrisData.objects.filter(owner=request.user).values_list(
            'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species', 'location'
        )
        
        for record in records:
            writer.writerow(record)
            
        return response


class IrisCSVImportView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file:
            messages.error(request, 'Lütfen bir dosya seçin.')
            return redirect('iris_listele')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Lütfen geçerli bir CSV dosyası yükleyin.')
            return redirect('iris_listele')
        
        try:
            #Dosyayı okuma kısmını burda yapıyorum
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            
            success_count = 0
            
            for line in lines[1:]:
                if not line.strip(): continue #Boş satırları atladım
                
                fields = line.split(",")
                if len(fields) >= 5:
                    IrisData.objects.create(
                        owner=request.user,
                        sepal_length=float(fields[0]),
                        sepal_width=float(fields[1]),
                        petal_length=float(fields[2]),
                        petal_width=float(fields[3]),
                        species=fields[4].strip(),
                        location_id=int(fields[5]) if len(fields) > 5 and fields[5].strip() else None
                    )
                    success_count += 1
            
            messages.success(request, f'{success_count} kayıt başarıyla yüklendi.')
            
        except Exception as e:
            messages.error(request, f'Hata oluştu: {str(e)}')
            
        return redirect('iris_listele')