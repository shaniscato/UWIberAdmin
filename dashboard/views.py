from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from django.db.models import Sum, Avg, Count
from itertools import chain
import datetime
from datetime import date

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

    """rides = Ride.objects.all()
    for ride in rides:
        name = ride.start_location.locationName
        location_count = rides.filter(start_location__locationName=name).count()"""

    locations = Location.objects.all()
    location_counter = []
    for location in locations:
        location_counter.append(rides.filter(start_location=location).count() + rides.filter(end_location=location).count())
    str(location_counter)

    drivers_weekly_avg = Ride.objects.filter(date_created__week=current_week).aggregate(Avg('price'))
    avg_week_income = drivers_weekly_avg['price__avg']

    """drivers_income = Driver.objects.filter(date_created__range=[start_week, end_week]).annotate(
        income=Sum('commission'))
    gross_income = drivers_income[0].income"""

    context = {'requests_per_month':requests_per_month,'locations': locations, 'location_counter':location_counter, 'requests_this_week': requests_this_week,
               'total_users': total_users, 'avg_week_income': avg_week_income, 'clients': clients[:3],
               'drivers': drivers[:3], 'rides': rides}

    return render(request, 'dashboard/dashboard.html', context)


def clients(request):
    return render(request, 'dashboard/clients.html')


def drivers(request):
    drivers = Driver.objects.all()
    return render(request, 'dashboard/drivers.html', {'drivers': drivers})


def driver_details(request, pk):
    driver = Driver.objects.get(id=pk)
    rides = driver.ride_set.all()

    clients = Client.objects.all()


    rides.filter(start_location='')
    ride_count = rides.count()
    scheduled_rides = rides.annotate(type=Count('ride_type')).count()
    commission = driver.commission
    unscheduled_rides = rides.annotate(type=Count('ride_type')).count()
    total_rides = scheduled_rides + unscheduled_rides



    context = {'driver': driver, 'rides': rides, 'ride_count': ride_count, 'scheduled_rides':scheduled_rides, 'unscheduled_rides':unscheduled_rides, 'total_rides':total_rides,'commission':commission}
    return render(request, 'dashboard/driverdetails.html', context)


def rides(request):
    rides = Ride.objects.all()
    return render(request, 'dashboard/rides.html', {'rides': rides})


def pie_chart(request):
    return render(request, 'dashboard/charts/piechart.html')


def line_graph(request):
    return render(request, 'dashboard/charts/linegraph.html')
