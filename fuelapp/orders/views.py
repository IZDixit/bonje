from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib import messages
from django.db import IntegrityError # Import the IntegrityError exception.
from .models import UserProfile, Order
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime
from .graph import create_customer_chart
from django.http import HttpResponse
from tablib import Dataset
from .resources import SalesRecordResource


# Create your views here.

def home(request):

    return render(request, 'main/index.html')

# - Register a User (This was done in step 1)
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Debugging line
            print("Form data: ", form.cleaned_data)
            try:
                user = form.save(commit=False) # Save without committing
                user.set_password(form.cleaned_data['password']) # Ensure password is hashed
                user.save() # commit the user instance


                # Create the UserProfile with the specified user_type
                # and set status to 'pending'
                user_profile = UserProfile.objects.create (
                    user=user,
                    user_type = form.cleaned_data['user_type'], # Set user_type based on form input
                    status='pending' if form.cleaned_data['user_type'] != 'manager' else 'approved' # setting status to 'pending' by default
                )
                # Debugging to check user_type
                print(f"Registering user {user.username} with type {form.cleaned_data['user_type']} and status {user_profile.status}")
                if user_profile.user_type == 'manager':
                    login(request, user) # We will login the manager automatically
                    return redirect('manager_dashboard')
                else:
                    return redirect('registration_pending')
            except IntegrityError:
                form.add_error(None, "A profile already exists for this user.")
                # Debugging line
                print("IntegrityError: A profile already exists")
    else:
        form = CreateUserForm()
    context = {'form':form}
    return render(request, 'main/register.html', context=context)
    

# Manager Approval View
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'manager')
def approve_users(request):
    # Get all pending user profiles
    pending_profiles = UserProfile.objects.filter(status='pending')

    if request.method == 'POST':
        if 'approve' in request.POST:
            user_ids = request.POST.getlist('user_ids') or [] # Fetch multiple user IDs hence we use ".getlist" 
                                                            # And take note that we are initializing as an empty list if no checkbox are selected.
            for user_id in user_ids:
                try:
                    profile = UserProfile.objects.get(user_id=user_id)
                    profile.status = 'approved'
                    profile.approved_date = timezone.now()
                    profile.save()
                    messages.success(request, f"User {profile.user.username} approved successfully")
                except UserProfile.DoesNotExist:
                    messages.error(request, f"User with ID {user_id} does not exist!")
                except Exception as e:
                    messages.error(request, f"Error approving user {user_id}: {str(e)}")
            return redirect('approve_users')
    
        elif 'reject' in request.POST:
            user_ids = request.POST.getlist('user_ids') or []
            for user_id in user_ids:
                try:
                    profile = UserProfile.objects.get(user_id=user_id)
                    profile.status = 'rejected'
                    profile.rejected = True
                    profile.save()
                    messages.success(request, f"User {profile.user.username} rejected successfully")
                except UserProfile.DoesNotExist:
                    messages.error(request, f"User with ID {user_id}: {str(e)}")
                return redirect('approve_users')
            
    return render(request, 'main/approve_user.html', {'profiles': pending_profiles})

# Manager disable user temporarily and permanently.
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'manager')
def approved_users(request):
    approved_profiles = UserProfile.objects.filter(status='approved')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        try:
            profile = UserProfile.objects.get(user_id=user_id)
            if action == 'disable_temp':
                profile.status = 'pending'
                profile.save()
                messages.success(request, f"User {profile.user.username} temporarily disabled.")
            elif action == 'disable_perm':
                profile.status = 'rejected'
                # profile.rejected = True
                profile.save()
                messages.success(request, f"User {profile.user.username} permanently disabled.")
        except UserProfile.DoesNotExist:
            messages.error(request, f"User with ID {user_id} does not exist!")
        return redirect('approved_users')

    return render(request, 'main/approved_users.html', {'profiles': approved_profiles})

# Manager, This will list out all rejected users.
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'manager')
def cancelled_approvals(request):
    cancelled_profiles = UserProfile.objects.filter(status="rejected")
    return render(request, 'main/cancelled_approvals.html', {'profiles': cancelled_profiles})
            
        
# Registration pending

def registration_pending(request):
    context = {
        'message': 'Your registration is pending approval. Please wait for confirmation'
    }
    return render(request, 'main/registration_pending.html', context=context)


# - Log-In a User
def my_login(request):

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if the user's profile status id 'pending'
                if hasattr(user, 'userprofile') and user.userprofile.status == 'pending':
                    messages.error(request, "Your account is pending approval.")
                    return redirect('my-login')

                print(f"Authenticated User at login: {user.username}")  # Debugging line

                # Login the User
                auth.login(request, user)

                # Check for associated user profile
                if hasattr(user, 'userprofile'):
                    print(f"User type at login: {user.userprofile.user_type}")
                    # Redirect based on user_type
                    # safely access user_type
                    # default to customer if no profile found
                    user_type = getattr(user.userprofile, 'user_type','customer')
                    # Redirect to manager dashboard
                    if user_type == 'manager':
                        return redirect('manager_dashboard')
                    # Redirect to supervisor dashboard
                    elif user_type == 'supervisor':
                        return redirect('supervisor_dashboard')
                    elif user_type == 'customer':
                        return redirect('customer_dashboard')
                    else:
                        return redirect("main_dashboard")
                else:
                    print("No user profile found for this user")
                    return redirect("main_dashboard")
                    
            else:
                messages.error(request, "Invalid username or password")
            
    context = {'form':form}

    return render(request, 'main/my-login.html', context=context)

# DASHBOARDS!
@login_required(login_url='my-login')
def dashboard(request):
    if request.user.is_authenticated:
        # safely access user_type
        user_type = request.user.userprofile.user_type #getattr(request.user.userprofile, 'user_type', '')
        # Debugging
        print(f"User type: {user_type}")

        #Determine which template to use based on user type
        if user_type == 'manager':
            return render(request, 'manager/dashboard.html')
        elif user_type == 'supervisor':
            return render(request, 'supervisor/dashboard.html')
        elif user_type == 'customer':
            return render(request, 'customer/dashboard.html')
        else:
            return render(request, 'main/dashboard.html') # Default Template
    else:
        return redirect('my-login')
# Manager, Dashboard
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'manager')   
def manager_dashboard(request):
    # Table part.
    # Sum of quantities grouped by user
    customer_totals = (
        Order.objects.values('user__username')
        .annotate(total_quantity=Sum('quantity'))
    )
    if request.method == 'POST':
        # Handle batch open or close action
        action = request.POST.get('action')
        selected_user_ids = request.POST.getlist('user_ids')

        if selected_user_ids:
            for user_id in selected_user_ids:
                orders = Order.objects.filter(user_id=user_id)
                if action == 'open':
                    orders.update(account_status='open')
                elif action == 'close':
                    orders.update(account_status='closed')
            messages.success(request, f"Account successfully {action}.")
        else:
            messages.warning(request, "No users selected.")
        return redirect('manager_dashboard')
    # Graph part
    # Filtering
    date_filter = request.GET.get('date')
    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year')

    # Filter customer orders based on selected date, month, or year
    orders = Order.objects.all()
    if date_filter:
        orders = orders.filter(created_at__date=date_filter)
    elif month_filter:
        orders = orders.filter(created_at__month=month_filter)
    elif year_filter:
        orders = orders.filter(created_at__year=year_filter)

    # Aggregate total quantity per customer
    # already did it above in the table part.^

    # Prepare data for Chart.js (We have switched to Matplotlib)
    chart_labels = [item['user__username'] for item in customer_totals]
    chart_data = [item['total_quantity'] for item in customer_totals]

    # Generate Chart image (using function in graph.py file)
    chart_image = create_customer_chart(chart_labels, chart_data)

    context = {
        'customer_totals': customer_totals,
        'chart_image': chart_image,
    }
    return render(request, 'manager/dashboard.html', context)

# Supervisor, Dashboard
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'supervisor')
def supervisor_dashboard(request):
    customers_orders = Order.objects.select_related('user').all().order_by('user__username')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('order_status')
        try:
            order = Order.objects.get(id=order_id)
            order.order_status = new_status
            order.save()
            messages.success(request, f"Order {order_id} status updated to {new_status}")
        except Order.DoesNotExist:
            messages.error(request, f"Order with ID {order_id} does not exist.")
        # return redirect('supervisor_dashboard')
    context = {'customers_orders': customers_orders}
    return render(request, 'supervisor/dashboard.html', context)

# Customer Dashboard.
@login_required
def customer_dashboard(request):
    # Filter Orders to show those of the logged in user only.
    
    my_orders = Order.objects.filter(user=request.user)
    context = {'orders': my_orders}
    
    return render(request, 'customer/dashboard.html', context)

def main_dashboard(request):
    return render(request, 'main/dashboard.html')

    # - User Logout

def user_logout(request):

    auth.logout(request)
    messages.success(request, "Logged out successfully.")

    return redirect("my-login")

# CUSTOMER FUNCTIONALITY.
# Customer, Create Order

@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'customer')
def create_record(request):

    form = CreateRecordForm()

    if request.method == 'POST':
        form = CreateRecordForm(request.POST)

        if form.is_valid():
            # Don't save the form directly; 
            # Create an instance to assign user (otherwise IntegrityError)
            order = form.save(commit=False)
            order.user = request.user # Assign the logged in user
            order.save()

            return redirect("customer_dashboard")
        
    context = {
        'form': form,
    }

    return render(request, 'customer/create-record.html', context)

# Customer, Update order, make corrections
# We will only allow this if order_status != collected.
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'customer')
def update_record(request, pk):

    order = get_object_or_404(Order, id=pk)

    # Check if the order status is collected
    if order.order_status == 'collected':
        messages.error(request, "This order has already been collected and cannot be edited.")
        return redirect("customer_dashboard")
    
    form = UpdateRecordForm(instance=order)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=order)

        if form.is_valid():
            # Assign User and save the order.
            order = form.save(commit=False)
            order.user = request.user # Assign the logged in user
            order.save()

            return redirect("customer_dashboard")
        
    context = {
        'form': form,
    }

    return render(request, 'customer/update-record.html', context)


# Link to the update order functionality
# Read or view a singular record.
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'customer')
def singular_record(request, pk):
    
    all_records = Order.objects.get(id=pk)

    context = {
        'order': all_records,
        }

    return render(request, 'customer/view-record.html', context)

# Delete an order, only if it is != 'collected'
# Customer, Delete order placed.
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'customer')
def delete_record(request, pk):

    order = get_object_or_404(Order, id=pk)

    # Check if order status is 'collected'
    if order.order_status == 'collected':
        messages.error(request, "This order has already been collected and cannot be deleted.")
        return redirect("customer_dashboard")
    
    # If not collected, delete order.
    order.delete()
    messages.success(request, "Order Successfully deleted.")

    return redirect("customer_dashboard")

    
# Importing my SalesRecord (sales by customer details) model
# Will be done by manager profile
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'manager')
def import_sales_record(request):
    """
    Handles the import of sales records from a CSV file for managers.

    This view checks if the request method is POST and processes the uploaded
    file. It uses the SalesRecordResource to load and validate the data from
    the CSV file. If the data is valid, it imports the sales records into the
    database. Otherwise, it returns an error message indicating the issues
    encountered during the import.

    Returns:
        HttpResponse: Success message if data is imported successfully, or an
        error message if the import fails.
    """
    if request.method == 'POST':
        sales_record_resource = SalesRecordResource()
        dataset = Dataset()
        new_sales_records = request.FILES['myfile']

        if new_sales_records.name.endswith('csv'):
            imported_data = dataset.load(new_sales_records.read().decode('utf-8'), format='csv')
            result = sales_record_resource.import_data(dataset, dry_run=True)

            if not result.has_errors():
                sales_record_resource.import_data(dataset, dry_run=False)

                return HttpResponse("Data imported successfully")
            
            else:
                errors = result.errors
                return HttpResponse(f"Error importing data {errors}")
            
    return render(request, 'manager/import-sales-record.html')