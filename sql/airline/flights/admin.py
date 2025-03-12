from django.contrib import admin

# Register your models here.
from .models import Airport, Flight 

admin.site.register(Airport)
admin.site.register(Flight)