from django.shortcuts import render
# Create your views here.


def home(request):
    return render(request, 'dashboard/dashboard.html')


def clients(request):
    return render(request, 'dashboard/clients.html')


def drivers(request):
    return render(request, 'dashboard/drivers.html')


def rides(request):
    return render(request, 'dashboard/rides.html')