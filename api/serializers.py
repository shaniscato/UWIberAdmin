from rest_framework import serializers
from dashboard.models import *
from django.contrib.auth.models import User


# class DriverSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=True)
#
#     class Meta:
#         model = Driver
#         fields = '__all__'
#         lookup_field = 'user__username'

class RideSerializer(serializers.ModelSerializer):
    start_location = serializers.StringRelatedField()
    end_location = serializers.StringRelatedField()

    class Meta:
        model = Ride
        fields = ['price', 'time', 'numPassengers', 'date_created', 'ride_type', 'start_location', 'end_location']


class ClientSerializer(serializers.ModelSerializer):
    ride_set = RideSerializer(many=True)

    class Meta:
        model = Client
        fields = ['date_of_birth', 'gender', 'phone_number', 'address', 'ride_set']


class UserSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'client']


# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = '__all__'
#
#
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ClientRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['user', 'gender', 'date_of_birth', 'phone_number', 'address']


class UserClientRegSerializer(serializers.ModelSerializer):
    client = ClientRegSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username',  'email', 'first_name', 'last_name', 'password', 'client']
        extra_kwargs = {"password": {'write_only': True}}

        def create(self, validated_data):
            print(validated_data)
            details = validated_data.pop('client')
            print(details)
            user = User.objects.create_user(**validated_data)
            for detail in details:
                print(detail)
                Client.objects.create(user=user, **detail)

            return user


# class ClientRegSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = '__all__'
#
#         def create(self, validated_data):
#             # Creates and returns a new user
#
#             client = Client(
#
#                 is_client=validated_data['is_client'],
#                 gender=validated_data['gender'],
#                 date_of_birth=validated_data['date_of_birth'],
#                 phone_number=validated_data['phone_number'],
#                 address=validated_data['address']
#
#             )
#             client.save()





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


