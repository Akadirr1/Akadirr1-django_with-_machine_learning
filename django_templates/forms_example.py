# Django Formları - Iris Sınıflandırma Sistemi
# Bu dosyayı Django projenizin forms.py dosyasına kopyalayın veya adapte edin

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import IrisRecord, Location, UserProfile


class UserRegistrationForm(UserCreationForm):
    """Kullanıcı kayıt formu"""
    email = forms.EmailField(required=True, label='E-posta')
    phone = forms.CharField(max_length=20, required=False, label='Telefon Numarası')
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Hakkında')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Kullanıcı Adı',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # UserProfile.objects.create(
            #     user=user,
            #     phone_number=self.cleaned_data.get('phone'),
            #     bio=self.cleaned_data.get('bio')
            # )
        return user


class IrisForm(forms.Form):
    """Iris kayıt formu"""
    SPECIES_CHOICES = [
        ('', 'Tür Seçiniz'),
        ('Iris-setosa', 'Iris Setosa'),
        ('Iris-versicolor', 'Iris Versicolor'),
        ('Iris-virginica', 'Iris Virginica'),
    ]

    sepal_length = forms.FloatField(
        label='Çanak Yaprağı Uzunluğu (cm)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'placeholder': 'Örn: 5.1'
        })
    )
    sepal_width = forms.FloatField(
        label='Çanak Yaprağı Genişliği (cm)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'placeholder': 'Örn: 3.5'
        })
    )
    petal_length = forms.FloatField(
        label='Taç Yaprağı Uzunluğu (cm)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'placeholder': 'Örn: 1.4'
        })
    )
    petal_width = forms.FloatField(
        label='Taç Yaprağı Genişliği (cm)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'placeholder': 'Örn: 0.2'
        })
    )
    species = forms.ChoiceField(
        label='Tür',
        choices=SPECIES_CHOICES
    )
    location = forms.IntegerField(
        label='Lokasyon',
        required=True,
        widget=forms.Select()
    )


class LocationForm(forms.Form):
    """Lokasyon formu"""
    name = forms.CharField(
        max_length=200,
        label='Lokasyon İsmi',
        widget=forms.TextInput(attrs={'placeholder': 'Örn: Merkez Park'})
    )
    city = forms.CharField(
        max_length=100,
        label='Şehir',
        widget=forms.TextInput(attrs={'placeholder': 'Örn: İstanbul'})
    )
    country = forms.CharField(
        max_length=100,
        label='Ülke',
        widget=forms.TextInput(attrs={'placeholder': 'Örn: Türkiye'})
    )
    elevation = forms.IntegerField(
        label='Yükseklik (m)',
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Örn: 100'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Lokasyon hakkında açıklama...'
        }),
        required=False,
        label='Açıklama'
    )


class TahminForm(forms.Form):
    """ML Tahmin formu"""
    MODEL_CHOICES = [
        ('', 'Model Seçiniz'),
        ('knn', 'K-En Yakın Komşu (KNN)'),
        ('svm', 'Destek Vektör Makinesi (SVM)'),
        ('decision_tree', 'Karar Ağacı Sınıflandırıcı'),
    ]

    ml_model = forms.ChoiceField(
        label='Makine Öğrenmesi Modeli',
        choices=MODEL_CHOICES
    )
    sepal_length = forms.FloatField(
        label='Çanak Yaprağı Uzunluğu (cm)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'placeholder': 'Örn: 5.1'
        })
    )
    sepal_width = forms.FloatField(
        label='Çanak Yaprağı Genişliği (cm)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'placeholder': 'Örn: 3.5'
        })
    )
    petal_length = forms.FloatField(
        label='Taç Yaprağı Uzunluğu (cm)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'placeholder': 'Örn: 1.4'
        })
    )
    petal_width = forms.FloatField(
        label='Taç Yaprağı Genişliği (cm)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'placeholder': 'Örn: 0.2'
        })
    )
