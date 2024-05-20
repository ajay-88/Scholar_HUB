from rest_framework import serializers

from .models import *

from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token


class AdminRegistrationserializer(serializers.ModelSerializer):
    class Meta:
        model=Profiledb
        fields=["username","password","email"]

    
class StudentRegistrationserializer(serializers.ModelSerializer):
    class Meta:
        model=Profiledb
        fields=["username","first_name","last_name","email","password","phone","address"]

class Commonloginserializer(serializers.Serializer): #generating token for login too
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self, attrs):
        username=attrs.get('username')
        password=attrs.get('password')
        user=authenticate(username=username,password=password)
        if not user:
            raise serializers.ValidationError("incorrect credentials")
        attrs['user']=user
        return attrs
    


class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = [ 'name', 'description', 'eligibility', 'amount', 'duration', 'deadline']

class StudentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentApplication
        fields = [ 'name', 'email', 'phone', 'application_date', 'certificate', 'identity', 'photo', 'scholarship', 'status']

        read_only_fields=["id"]

class StudentApplicationSerializerUP(serializers.ModelSerializer):
    class Meta:
        model = StudentApplication
        fields = ['status']

        read_only_fields=["id"]

        



