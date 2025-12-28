from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	bio = models.TextField(null=True,blank=True)
	phone_number = models.CharField(null=True,max_length=11,blank=True)
	birth_date=models.DateField(null=True,blank=True)
	
	#veritabanında burası required olmuyor blank sayesinde ve null alabiliyorlar
	def __str__(self):
		return self.username