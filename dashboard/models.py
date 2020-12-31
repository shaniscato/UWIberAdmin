from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.


class AppUser(models.Model):
    username = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=60, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_logged_in = models.DateTimeField(null=True)
    first_name = models.CharField(max_length=16, null=True)
    last_name = models.CharField(max_length=16, null=True)
    date_of_birth = models.DateField(max_length=40, null=True)
    gender = models.CharField(max_length=1, null=True)
    phone_number = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    profile_picture = models.FileField(upload_to='files', null=True)

    class Meta:
        abstract = True
        ordering = ['date_created']


class Client(AppUser):
    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.first_name + " " + self.last_name


class Vehicle(models.Model):
    carMake = models.CharField(max_length=40, null=True)
    carModel = models.CharField(max_length=200, null=True)
    carCapacity = models.IntegerField(null=True)

    def __str__(self):
        return self.carMake + " " + self.carModel


class Driver(AppUser):
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.SET_NULL)
    commission = models.FloatField(null=True)
    scheduled_rides = models.IntegerField(null=True)
    unscheduled_rides = models.IntegerField(null=True)
    total_rides = models.IntegerField(null=True)
    documentation = models.FileField(upload_to='files', null=True)
    license_issue_date = models.DateField(null=True)
    license_expiry_date = models.DateField(null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Location(models.Model):
    locationName = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.locationName


class Ride(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(Driver, null=True, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    STATUS = (
        ('Pending Pickup', 'Pending Pickup'),
        ('Pickup Location', 'Pickup Location'),
        ('Pending Drop-off', 'Pending Drop-off'),
        ('Drop-off Location', 'Drop-off Location')
    )

    price = models.FloatField(null=True)
    time = models.TimeField(null=True)
    numPassengers = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return str(self.date_created) + " - " + str(self.driver)