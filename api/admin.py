from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.
class CustomUserAdmin(UserAdmin):
	fieldsets=UserAdmin.fieldsets + (('Özel Bilgiler',{'fields':('bio','phone_number','birth_date')}),)
	add_fieldsets=UserAdmin.add_fieldsets + ((None,{'fields':('bio','phone_number','birth_date')}),)
admin.site.register(CustomUser,CustomUserAdmin)