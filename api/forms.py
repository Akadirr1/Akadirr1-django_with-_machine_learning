# Django Formları - Iris Sınıflandırma Sistemi

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, IrisData, Location


class UserRegistrationForm(UserCreationForm):
    """Kullanıcı kayıt formu"""
    email = forms.EmailField(required=True, label='E-posta')
    phone_number = forms.CharField(max_length=20, required=False, label='Telefon Numarası')
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Hakkında')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'bio']
        labels = {
            'username': 'Kullanıcı Adı',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number')
        user.bio = self.cleaned_data.get('bio')
        if commit:
            user.save()
        return user


class IrisForm(forms.ModelForm):
    """Iris kayıt formu"""
    class Meta:
        model = IrisData
        fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species', 'location']
        widgets = {
            'sepal_length': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'placeholder': 'Örn: 5.1'
            }),
            'sepal_width': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'placeholder': 'Örn: 3.5'
            }),
            'petal_length': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'placeholder': 'Örn: 1.4'
            }),
            'petal_width': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'placeholder': 'Örn: 0.2'
            }),
        }


class LocationForm(forms.ModelForm):
    """Lokasyon formu"""
    class Meta:
        model = Location
        fields = ['name', 'city', 'country', 'elevation', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Örn: Merkez Park'}),
            'city': forms.TextInput(attrs={'placeholder': 'Örn: İstanbul'}),
            'country': forms.TextInput(attrs={'placeholder': 'Örn: Türkiye'}),
            'elevation': forms.NumberInput(attrs={'placeholder': 'Örn: 100', 'min': '0'}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Lokasyon hakkında açıklama...'
            }),
        }


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
