from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Location
from .models import IrisData
# Register your models here.
class CustomUserAdmin(UserAdmin):
	fieldsets=UserAdmin.fieldsets + (('Özel Bilgiler',{'fields':('bio','phone_number','birth_date')}),)
	add_fieldsets=UserAdmin.add_fieldsets + ((None,{'fields':('bio','phone_number','birth_date')}),)
	list_display = ('username', 'email', 'phone_number', 'is_staff')
admin.site.register(CustomUser,CustomUserAdmin)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display=('name','city','country','elevation')
	search_fields=('name','city')
	list_filter=('country',)
@admin.register(IrisData)
class IrisDataAdmin(admin.ModelAdmin):
	list_display=('species', 'owner', 'location', 'sepal_length', 'created_at')
	list_display_links = ('species',)
	list_filter=('species','location')
	search_fields=('species', 'owner__username', 'location__name')