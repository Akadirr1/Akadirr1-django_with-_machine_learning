# Django Modelleri - Iris Sınıflandırma Sistemi
# Bu dosyayı Django projenizin models.py dosyasına kopyalayın veya adapte edin

from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    """Lokasyon modeli"""
    name = models.CharField(max_length=200, verbose_name='İsim')
    city = models.CharField(max_length=100, verbose_name='Şehir')
    country = models.CharField(max_length=100, verbose_name='Ülke')
    elevation = models.IntegerField(verbose_name='Yükseklik (m)')
    description = models.TextField(blank=True, null=True, verbose_name='Açıklama')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lokasyon'
        verbose_name_plural = 'Lokasyonlar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"


class IrisRecord(models.Model):
    """Iris kaydı modeli"""
    SPECIES_CHOICES = [
        ('Iris-setosa', 'Iris Setosa'),
        ('Iris-versicolor', 'Iris Versicolor'),
        ('Iris-virginica', 'Iris Virginica'),
    ]

    sepal_length = models.FloatField(verbose_name='Çanak Yaprağı Uzunluğu (cm)')
    sepal_width = models.FloatField(verbose_name='Çanak Yaprağı Genişliği (cm)')
    petal_length = models.FloatField(verbose_name='Taç Yaprağı Uzunluğu (cm)')
    petal_width = models.FloatField(verbose_name='Taç Yaprağı Genişliği (cm)')
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES, verbose_name='Tür')
    location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Lokasyon',
        related_name='iris_records'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Oluşturan',
        related_name='iris_records'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Iris Kaydı'
        verbose_name_plural = 'Iris Kayıtları'
        ordering = ['-created_at']

    def __str__(self):
        return f"Iris #{self.id} - {self.species}"


class UserProfile(models.Model):
    """Kullanıcı profil modeli"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefon')
    bio = models.TextField(blank=True, null=True, verbose_name='Hakkında')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Kullanıcı Profili'
        verbose_name_plural = 'Kullanıcı Profilleri'

    def __str__(self):
        return f"{self.user.username} Profili"
