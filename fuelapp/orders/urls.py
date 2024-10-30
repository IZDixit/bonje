from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=''),
    
    path('register/', views.register, name="register"),

    path('approve-users/', views.approve_users, name='approve_users'),

    path('approved-users/', views.approved_users, name='approved_users'),

    path('cancelled-approvals/', views.cancelled_approvals, name='cancelled_approvals'),

    path('registration-pending/', views.registration_pending, name='registration_pending'),

    path('my-login/', views.my_login, name='my-login'),

    path('user-logout', views.user_logout, name="user-logout"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('manager/dashboard/', views.manager_dashboard, name="manager_dashboard"),

    path('supervisor/dashboard/', views.supervisor_dashboard, name="supervisor_dashboard"),

    path('customer/dashboard/', views.customer_dashboard, name="customer_dashboard"),

    path('main/dashboard/', views.main_dashboard, name="main_dashboard"),

    path('customer/create-record/', views.create_record, name="create_record"),

    path('customer/update-record/<int:pk>/', views.update_record, name="update_record"),

    path('record/<int:pk>/', views.singular_record, name="record"),

    path('delete-record/<int:pk>/', views.delete_record, name="delete_record"),

]