from rest_framework import serializers
from dashboard.models import *


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'


class ClientRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {"password": {'write_only': True}}

        def create(self, validated_data):
            # Creates and returns a new user

            user = Client(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password'],
                is_client=validated_data['is_client']
            )
            user.save()


class DriverRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
        extra_kwargs = {"password": {'write_only': True}}

        def create(self, validated_data):
            # Creates and returns a new user

            user = Driver(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password'],
                is_client=validated_data['is_client']
            )
            user.save()
