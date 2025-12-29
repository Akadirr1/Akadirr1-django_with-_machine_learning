# Django Views - Iris Sınıflandırma Sistemi
# Bu dosyayı Django projenizin views.py dosyasına kopyalayın veya adapte edin

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
# from .models import IrisRecord, Location  # Modellerinizi import edin
# from .forms import IrisForm, LocationForm, UserRegistrationForm  # Formlarınızı import edin


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
        # Form işleme mantığı
        # form = UserRegistrationForm(request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
        #     return redirect('index')
        pass
    
    return render(request, 'kayit.html')


@login_required
def iris_ekle(request):
    """Yeni Iris ekleme view"""
    # locations = Location.objects.all()
    locations = []  # Geçici boş liste
    
    if request.method == 'POST':
        # Form işleme mantığı
        # form = IrisForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     messages.success(request, 'Iris örneği başarıyla eklendi!')
        #     return redirect('iris_listele')
        pass
    
    return render(request, 'iris_ekle.html', {
        'locations': locations,
    })


@login_required
def iris_listele(request):
    """Iris kayıtlarını listeleme view"""
    # records = IrisRecord.objects.all()
    records = []  # Geçici boş liste
    
    return render(request, 'iris_listele.html', {
        'records': records,
    })


@login_required
def iris_guncelle(request, id):
    """Iris güncelleme view"""
    # record = get_object_or_404(IrisRecord, id=id)
    record = None  # Geçici
    
    if request.method == 'POST':
        # Form işleme mantığı
        # form = IrisForm(request.POST, instance=record)
        # if form.is_valid():
        #     form.save()
        #     messages.success(request, 'Iris örneği başarıyla güncellendi!')
        #     return redirect('iris_listele')
        pass
    
    return render(request, 'iris_guncelle.html', {
        'record': record,
    })


@login_required
def iris_sil(request, id):
    """Iris silme view"""
    # record = get_object_or_404(IrisRecord, id=id)
    record = None  # Geçici
    
    if request.method == 'POST':
        # record.delete()
        # messages.success(request, 'Iris örneği başarıyla silindi!')
        # return redirect('iris_listele')
        pass
    
    return render(request, 'iris_sil.html', {
        'record': record,
    })


@login_required
def location_ekle(request):
    """Yeni lokasyon ekleme view"""
    if request.method == 'POST':
        # Form işleme mantığı
        # form = LocationForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     messages.success(request, 'Lokasyon başarıyla eklendi!')
        #     return redirect('location_listele')
        pass
    
    return render(request, 'location_ekle.html')


@login_required
def location_listele(request):
    """Lokasyonları listeleme view"""
    # locations = Location.objects.all()
    locations = []  # Geçici boş liste
    
    return render(request, 'location_listele.html', {
        'locations': locations,
    })


@login_required
def location_sil(request, id):
    """Lokasyon silme view"""
    # location = get_object_or_404(Location, id=id)
    location = None  # Geçici
    
    if request.method == 'POST':
        # location.delete()
        # messages.success(request, 'Lokasyon başarıyla silindi!')
        # return redirect('location_listele')
        pass
    
    return render(request, 'location_sil.html', {
        'location': location,
    })


@login_required
def tahmin(request):
    """ML Tahmin view"""
    prediction = None
    model_name = None
    
    model_names = {
        'knn': 'K-En Yakın Komşu (KNN)',
        'svm': 'Destek Vektör Makinesi (SVM)',
        'decision_tree': 'Karar Ağacı Sınıflandırıcı'
    }
    
    if request.method == 'POST':
        ml_model = request.POST.get('ml_model')
        sepal_length = float(request.POST.get('sepal_length'))
        sepal_width = float(request.POST.get('sepal_width'))
        petal_length = float(request.POST.get('petal_length'))
        petal_width = float(request.POST.get('petal_width'))
        
        # ML tahmin mantığı burada olacak
        # prediction = predict_iris_species(ml_model, sepal_length, sepal_width, petal_length, petal_width)
        prediction = "Iris-setosa"  # Geçici örnek
        model_name = model_names.get(ml_model, ml_model)
    
    return render(request, 'tahmin.html', {
        'prediction': prediction,
        'model_name': model_name,
    })
