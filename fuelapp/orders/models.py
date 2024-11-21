from django.db import models
from django.contrib.auth.models import User
from import_export import resources


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
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('collected', 'Collected'),
        ('on hold', 'On Hold'),
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
    account_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username} at {self.created_at}"

# The below model will allow us to import the sales by customer file 
# and export it after we have edited as needed.
# We will access this via the class in resources.py file.
class SalesRecord(models.Model):
    id = models.AutoField(primary_key=True)
    Type = models.CharField(blank=True, null=True, max_length=100)
    Date = models.DateField()
    Num = models.CharField(blank=True, null=True, max_length=50)
    Name = models.CharField(blank=True, null=True, max_length=200)
    Memo = models.CharField(blank=True, null=True, max_length=50)
    Item = models.CharField(max_length=100)
    Qty = models.IntegerField()
    Sales_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id} - {self.Name}"