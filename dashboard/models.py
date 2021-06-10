from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, User


# Create your models here.


class Vehicle(models.Model):
    carMake = models.CharField(max_length=40, null=True)
    carModel = models.CharField(max_length=200, null=True)
    carCapacity = models.IntegerField(null=True)

    def __str__(self):
        return self.carMake + " " + self.carModel


class CustomUser(models.Model):
    # username = models.CharField(max_length=20, null=True)
    # email = models.CharField(max_length=60, null=True)
    # is_client = models.BooleanField(default=True)
    # date_created = models.DateTimeField(auto_now_add=True, null=True)
    # last_logged_in = models.DateTimeField(null=True)
    # first_name = models.CharField(max_length=16, null=True)
    # last_name = models.CharField(max_length=16, null=True)
    date_of_birth = models.DateField(max_length=40, null=True)
    gender = models.CharField(max_length=1, null=True)
    phone_number = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)

    class Meta:
        abstract = True


class Client(CustomUser):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='client')

    def __str__(self):
        template = '{0.user.first_name} {0.user.last_name}'
        return template.format(self)
    #     return str(self.user)

    # list_display = ("last_name", "first_name")



class Driver(CustomUser):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.SET_NULL)
    commission = models.FloatField(null=True)
    scheduled_rides = models.IntegerField(null=True)
    unscheduled_rides = models.IntegerField(null=True)
    documentation = models.FileField(upload_to='files', null=True)
    license_issue_date = models.DateField(null=True)
    license_expiry_date = models.DateField(null=True)

    def __str__(self):
        template = '{0.user.first_name} {0.user.last_name}'
        return template.format(self)

    # def __str__(self):
    #     return str(self.user)


class Location(models.Model):
    locationName = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.locationName


class Ride(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(Driver, null=True, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.SET_NULL)
    start_location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL, related_name='start_location')
    end_location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL, related_name='end_location')
    STATUS = (
        ('Pending Pickup', 'Pending Pickup'),
        ('Pickup Location', 'Pickup Location'),
        ('Pending Drop-off', 'Pending Drop-off'),
        ('Drop-off Location', 'Drop-off Location')
    )
    TYPE = (
        ('Scheduled Ride', 'Scheduled Ride'),
        ('Unscheduled Ride', 'Unscheduled Ride'),
    )
    price = models.FloatField(null=True)
    time = models.TimeField(null=True)
    numPassengers = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    ride_type = models.CharField(max_length=200, null=True, choices=TYPE)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        template = '{0.start_location}-{0.end_location} {0.time}'
        return template.format(self)


class UserManager(models.Manager):
    def create(self, username, gender):
        user = User(username=username, gender=gender)
        user.save()
        client = Client(user=user, gender=gender)
        client.save()
        return user
