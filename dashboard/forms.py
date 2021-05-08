from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('is_client',)


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
        exclude = ('is_client',)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
