from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	bio = models.TextField(null=True,blank=True)
	phone_number = models.CharField(null=True,max_length=11,blank=True)
	birth_date=models.DateField(null=True,blank=True)
	
	#veritabanında burası required olmuyor blank sayesinde ve null alabiliyorlar
	def __str__(self):
		return self.username
class Location(models.Model):
	name=models.CharField(max_length=50,verbose_name="Bölge adı")
	city=models.CharField(max_length=50,verbose_name="Şehir")
	country=models.CharField(max_length=50,verbose_name="Ülke")
	elevation=models.IntegerField(default=0,verbose_name="Rakım")
	description=models.TextField(max_length=300,blank=True,null=True,verbose_name="Bölge açıklaması")
	def __str__(self):
		return f"{self.name} - ({self.city})"	
class IrisData(models.Model):
	TURLER = (
        ('Iris-setosa', 'Iris Setosa'),
        ('Iris-versicolor', 'Iris Versicolor'),
        ('Iris-virginica', 'Iris Virginica'),
    )
	sepal_length=models.FloatField(verbose_name="Çanak Yaprak Uzunluğu")
	sepal_width=models.FloatField(verbose_name="Çanak Yaprak genişliği")
	petal_length=models.FloatField(verbose_name="Taç Yaprak Uzunluğu")
	petal_width=models.FloatField(verbose_name="Taç Yaprak Genişliği")
	owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name="Kaydeden Kullanıcı")
	location=models.ForeignKey(Location,on_delete=models.CASCADE,verbose_name="Konum bilgis")
	species=models.CharField(max_length=50,choices=TURLER,verbose_name="Çiçek Türü")
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
def __str__(self):
	return f"{self.owner.username}-{self.species}"

