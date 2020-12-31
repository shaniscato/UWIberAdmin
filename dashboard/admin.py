from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Client)
admin.site.register(Ride)
admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Location)