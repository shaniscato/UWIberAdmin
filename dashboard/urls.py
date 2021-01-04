from django.urls import path
from django.conf import settings
from django.conf.urls import url, include

from dashboard import views

urlpatterns = [
    path('', views.home, name="home"),
    path('clients/', views.clients, name="clients"),
    path('clients/<str:pk>/', views.clients, name="clientdetails"),
    path('drivers/', views.drivers, name="drivers"),
    path('drivers/<str:pk>', views.driver_details, name="driverdetails"),
    path('rides/', views.rides, name="rides")

]