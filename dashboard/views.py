from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *
from django.db.models import Sum, Avg, Count
from itertools import chain
import datetime
from datetime import date
from .forms import *

from django.utils import timezone
import pytz

import datetime
from datetime import datetime, timedelta
# Create your views here.


def home(request):
    rides = Ride.objects.all()
    drivers = Driver.objects.all()
    clients = Client.objects.all()
    total_users = drivers.count() + clients.count()

    current_week = date.today().isocalendar()[1]
    requests_this_week = Ride.objects.filter(date_created__week=current_week).count()

    requests_per_month = []
    for month in range(1, 12):
        requests_per_month.append(Ride.objects.filter(date_created__month=month).count())
    str(requests_per_month)

    locations = Location.objects.all()
    location_counter = []
    for location in locations:
        location_counter.append(rides.filter(start_location=location).count() + rides.filter(end_location=location).count())
    str(location_counter)

    drivers_weekly_avg = Ride.objects.filter(date_created__week=current_week).aggregate(Avg('price'))
    avg_week_income = drivers_weekly_avg['price__avg']

    context = {'requests_per_month':requests_per_month,'locations': locations, 'location_counter':location_counter, 'requests_this_week': requests_this_week,
               'total_users': total_users, 'avg_week_income': avg_week_income, 'clients': clients[:3],
               'drivers': drivers[:3], 'rides': rides}

    return render(request, 'dashboard/dashboard.html', context)


def clients(request):
    clients = Client.objects.all()
    return render(request, 'dashboard/clients.html', {'clients':clients})


def drivers(request):
    drivers = Driver.objects.all()
    return render(request, 'dashboard/drivers.html', {'drivers': drivers})


def driver_details(request, pk):
    driver = Driver.objects.get(id=pk)
    rides = driver.ride_set.all()

    ride_count = rides.count()
    scheduled_rides = rides.annotate(type=Count('ride_type')).count()
    commission = driver.commission
    unscheduled_rides = rides.annotate(type=Count('ride_type')).count()
    total_rides = scheduled_rides + unscheduled_rides

    context = {'driver': driver, 'rides': rides, 'ride_count': ride_count, 'scheduled_rides':scheduled_rides, 'unscheduled_rides':unscheduled_rides, 'total_rides':total_rides,'commission':commission}
    return render(request, 'dashboard/driverdetails.html', context)


def client_details(request, pk):
    client = Client.objects.get(id=pk)
    rides = client.ride_set.all()
    ride_count = rides.count()
    context = {'client': client, 'rides': rides, 'ride_count': ride_count}
    return render(request, 'dashboard/clientdetails.html', context)


def rides(request):
    rides = Ride.objects.all()
    return render(request, 'dashboard/rides.html', {'rides': rides})


def pie_chart(request):
    return render(request, 'dashboard/charts/piechart.html')


def line_graph(request):
    return render(request, 'dashboard/charts/linegraph.html')

def create_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/clients')
    context = {'form':form}
    return render(request, 'dashboard/forms/clientform.html', context)


def update_client(request, pk):
    client = Client.objects.get(id=pk)
    form = ClientForm(instance=client)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('/clients')

    context = {'form': form}
    return render(request, 'dashboard/forms/clientform.html', context)


def create_driver(request):
    form = DriverForm()
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/drivers')
    context = {'form': form}
    return render(request, 'dashboard/forms/driverform.html', context)


def update_driver(request, pk):
    driver = Driver.objects.get(id=pk)
    form = DriverForm(instance=driver)

    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('/drivers')
    context = {'form': form}
    return render(request, 'dashboard/forms/driverform.html', context)
