from rest_framework import serializers
from .models import CustomUser

class HelloSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
class ToplamaSerializers(serializers.Serializer):
    sayi1=serializers.IntegerField()
    sayi2=serializers.IntegerField()
class IrisInputSerializer(serializers.Serializer):
    MODEL_SECENEKLERI=(('knn','KNN (En Yakın Komşu)'),
                       ('svm','SVM (Destek Vektör)'),
                       ('dt','Decision Tree(Karar ağacı)'))
    model_type=serializers.ChoiceField(choices=MODEL_SECENEKLERI,default='knn')
    sepal_length=serializers.FloatField()
    sepal_width=serializers.FloatField()
    petal_length=serializers.FloatField()
    petal_width=serializers.FloatField()
class RegisterSerializers(serializers.ModelSerializer):
	
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields=('username','email','password','bio','phone_number')#kullanıcıdan hangi bilgiler istenecek tanımladım
    def validate_email(self,value):
        if not value:
            raise serializers.ValidationError("Email Alanı Zorunludur!")
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email kayıtlı!")
        return value
    def create(self,validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email',''),
            password=validated_data['password'],
            bio=validated_data.get('bio',''),
            phone_number=validated_data.get('phone_number','')
		)
        return user