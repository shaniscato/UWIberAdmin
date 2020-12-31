from django.urls import path
from django.conf.urls import url, include

from dashboard import views

urlpatterns = [
    path('', views.home, name="home"),
    path('clients/', views.clients, name="clients"),
    path('drivers/', views.drivers, name="drivers"),
    path('rides/', views.drivers, name="rides"),

]