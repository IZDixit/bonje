from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=''),
    
    path('register/', views.register, name="register"),

    path('my-login', views.my_login, name='my-login'),

    path('user-logout', views.user_logout, name="user-logout"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('manager/dashboard/', views.manager_dashboard, name="manager_dashboard"),

    path('supervisor/dashboard/', views.supervisor_dashboard, name="supervisor_dashboard"),

    path('customer/dashboard/', views.customer_dashboard, name="customer_dashboard"),

    path('main/dashboard/', views.main_dashboard, name="main_dashboard"),
]