from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'url', 'username', 'email', 'fullname', 'title', 'avatar']
        read_only_fields = ('pk', 'username', 'email',)

#--> auth serializers
class UserRegistrationSerializer(serializers.Serializer):
    registration = serializers.CharField(required=True, label="Registration")
    firstname    = serializers.CharField(max_length=200)
    lastname    = serializers.CharField(max_length=200)
    organization = serializers.CharField(max_length=200)
    phone    = serializers.CharField(max_length=200)
    password    = serializers.CharField(required=True, label="Password", style={'input_type': 'password'})

    def save(self):
        registration = self.validated_data['registration']
        firstname    = self.validated_data['firstname']
        lastname    = self.validated_data['lastname']
        organization   = self.validated_data['organization']
        phone    = self.validated_data['phone']
        password = self.validated_data['password']
        user_obj = User(
                registration = registration,
                firstname = firstname,
                lastname = lastname,
                organization = organization,
                phone = phone
            )
        user_obj.set_password(password)
        user_obj.is_active = True
        user_obj.save()
        return user_obj

