from django.shortcuts import render, redirect
from django.db.models import Sum, Avg, Count
from datetime import date

from .decorators import unauthenticated_user, allowed_users
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models.functions import Coalesce

# Create your views here.


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save
            username = form.cleaned_data.get("username")
            group = Group.objects.get(name='Client')
            user.groups.add(group)
            messages.success(request, "Account was successfully created for "+ username )
            return redirect('login')
    context = {'form': form}
    return render(request, 'dashboard/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
            return render(request, 'dashboard/login.html')
    context = {}
    return render(request, 'dashboard/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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

    # drivers_weekly_avg = Ride.objects.filter(date_created__week=current_week).aggregate(Avg('price'))
    drivers_weekly_avg = Ride.objects.filter(date_created__week=current_week).aggregate(
        display_price=Coalesce(Avg('price'), 0))
    avg_week_income = drivers_weekly_avg['display_price']

    context = {'requests_per_month':requests_per_month,'locations': locations, 'location_counter':location_counter, 'requests_this_week': requests_this_week,
               'total_users': total_users, 'avg_week_income': avg_week_income, 'clients': clients[:3],
               'drivers': drivers[:3], 'rides': rides}

    return render(request, 'dashboard/dashboard.html', context)


def profile_page(request):
    context = {}
    return render(request, 'dashboard/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def clients(request):
    clients = Client.objects.all()
    return render(request, 'dashboard/clients.html', {'clients':clients})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def drivers(request):
    drivers = Driver.objects.all()
    return render(request, 'dashboard/drivers.html', {'drivers': drivers})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def driver_details(request, pk):
    driver = Driver.objects.get(id=pk)
    rides = driver.ride_set.all()

    ride_count = rides.count()
    scheduled_rides = rides.annotate(type=Count('ride_type')).count()
    commission = driver.commission
    unscheduled_rides = rides.annotate(type=Count('ride_type')).count()

    age = driver.date_of_birth

    total_rides = scheduled_rides + unscheduled_rides

    context = {'driver': driver, 'rides': rides, 'ride_count': ride_count, 'scheduled_rides':scheduled_rides, 'unscheduled_rides':unscheduled_rides, 'total_rides':total_rides,'commission':commission}
    return render(request, 'dashboard/driverdetails.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def create_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/clients')
    context = {'form':form}
    return render(request, 'dashboard/forms/clientform.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def create_driver(request):
    form = DriverForm()
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/drivers')
    context = {'form': form}
    return render(request, 'dashboard/forms/driverform.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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
