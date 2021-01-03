from django.shortcuts import render
from django.views.generic import TemplateView

from .models import *
from django.db.models import Sum, Avg
from itertools import chain
import datetime
from datetime import datetime
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

    utcnow = datetime.utcnow()
    date = utcnow.replace(tzinfo=pytz.utc)
    start_week = date - timezone.timedelta(date.weekday())
    end_week = start_week + timezone.timedelta(7)
    requests_this_week = Ride.objects.filter(date_created__range=[start_week, end_week]).count()

    rides = Ride.objects.all()
    for ride in rides:
        name = ride.start_location.locationName
        location_count = rides.filter(start_location__locationName=name).count()

    locations = Location.objects.all()

    drivers_weekly_avg = Ride.objects.filter(date_created__range=[start_week, end_week]).aggregate(Avg('price'))
    avg_week_income = drivers_weekly_avg['price__avg']

    drivers_income = Driver.objects.filter(date_created__range=[start_week, end_week]).annotate(income=Sum('commission'))
    gross_income = drivers_income[0].income

    context = {'location_count':location_count,'locations': locations, 'requests_this_week': requests_this_week, 'total_users': total_users, 'avg_week_income': avg_week_income, 'clients': clients[:3],'drivers': drivers[:3],'rides':rides}



    return render(request, 'dashboard/dashboard.html', context)


def clients(request):
    return render(request, 'dashboard/clients.html')


def drivers(request):
    drivers = Driver.objects.all()
    return render(request, 'dashboard/drivers.html', {'drivers': drivers})


def rides(request):
    rides = Ride.objects.all()
    return render(request, 'dashboard/rides.html', {'rides': rides})


def pie_chart(request):
    return render(request, 'dashboard/charts/piechart.html')


def line_graph(request):
    return render(request, 'dashboard/charts/linegraph.html')