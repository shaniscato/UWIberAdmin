from django.urls import path
from django.conf import settings
from django.conf.urls import url, include

from dashboard import views

urlpatterns = [
    path('', views.home, name="home"),
    path('clients/', views.clients, name="clients"),
    path('clients/<str:pk>/', views.client_details, name="clientdetails"),
    path('drivers/', views.drivers, name="drivers"),
    path('drivers/<str:pk>', views.driver_details, name="driverdetails"),
    path('rides/', views.rides, name="rides"),

    path('create-client/', views.create_client, name="create_client"),
    path('update-client/<str:pk>/', views.update_client, name="update_client"),
    path('create-driver/', views.create_client, name="create_driver"),
    path('update-driver/<str:pk>/', views.update_driver, name="update_driver"),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
]