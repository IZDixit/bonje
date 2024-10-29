from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('customer', 'Customer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15,blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('pending','Pending'), ('approved', 'Approved'), ('rejected','Rejected'), ('disabled','Disabled')], default='pending')

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"
    
# Applying orders.0002_userprofile_status_order... OK
class Order(models.Model):
    PRODUCT_CHOICES = [
        ('AGO', 'AGO'),
        ('UX','UX'),
        ('LUBRICANTS','LUBRICANTS'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(
        max_length=100,
        choices=PRODUCT_CHOICES,
        default='AGO'
    )
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    vehicle_number = models.CharField(
        max_length=20,
        help_text="Enter vehicle number (letter and numbers allowed)"
    )
    driver_name = models.CharField(
        max_length=100,
        blank=True, # This field is optional
        help_text="Enter driver's name (optional)"
    )
    driver_id_number = models.CharField(
        max_length=50,
        blank=True, # This field is optional
        help_text="Enter driver's ID number or Telephone (optional)"
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username} at {self.created_at}"
