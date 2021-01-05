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