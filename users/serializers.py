from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from phonenumber_field.modelfields import PhoneNumberField
from .models import User
from django.db import models

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User 
        fields = [              
            "email",
            "password",
            "username",
            "full_name",
            "phone_number",

        ]



class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = [              
            "full_name",
            "email",
            "phone_number",
        ]


class LoginInputSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
    password = serializers.CharField()




class TokenSerializer(serializers.Serializer):

    Token = serializers.CharField() 
    #TODO Clean


class FireBaseUserSerializer(serializers.Serializer):

    localId = serializers.CharField()
    email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
    displayName = serializers.CharField()
    passwordHash = serializers.CharField()
    emailVerified = serializers.CharField()
    passwordUpdatedAt = serializers.CharField()
    validSince = serializers.CharField()
    disabled = serializers.BooleanField()
    lastLoginAt = serializers.CharField()
    createdAt = serializers.CharField()
    phoneNumber = PhoneNumberField()
    lastRefreshAt = serializers.CharField()
    likes = serializers.IntegerField()


class AddressSerializer(serializers.Serializer):
    
    street_address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    pin = serializers.CharField()
    phone_number = PhoneNumberField()
    name = serializers.CharField()

    # Define clean functions.

class CustomerInfoSerializer(serializers.Serializer):

    address = AddressSerializer(many=True)


class RefreshToken(serializers.Serializer):

    refreshToken = serializers.CharField()
    


class FireBaseUserDataOutput(serializers.Serializer):
    
    localId = serializers.CharField()
    email = serializers.EmailField()
    displayName = serializers.CharField()
    passwordHash = serializers.CharField()
    emailVerified = serializers.BooleanField()
    passwordUpdatedAt = serializers.CharField()
    validSince = serializers.CharField()
    disabled = serializers.BooleanField()
    lastLoginAt = serializers.CharField()
    createdAt = serializers.CharField()
    phoneNumber = serializers.CharField()
    lastRefreshAt = serializers.CharField()


