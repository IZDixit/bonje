from django.contrib import admin

# Register your models here.

# importing my Order model, access from admin account
from . models import Order

admin.site.register(Order)
