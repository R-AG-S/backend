from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    full_name = serializers.CharField(max_length=50)
    phone_number = PhoneNumberField()

class UserEditSerializer(serializers.Serializer):

    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=50)
    phone_number = PhoneNumberField()

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




class CustomerInfoSerializer(serializers.Serializer):

    car_model = serializers.CharField()
    mileage = serializers.CharField()
    



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


