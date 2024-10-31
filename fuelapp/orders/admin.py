from django.contrib import admin

# Register your models here.

# importing my Order model, access from admin account
from . models import Order,UserProfile

admin.site.register(Order)
admin.site.register(UserProfile)
