from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CreateUserForm, LoginForm
from django.contrib import messages
from django.db import IntegrityError # Import the IntegrityError exception.
from .models import UserProfile
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
        user_ids = request.POST.get('user_ids')
        for user_id in user_ids:
            try:
                profile = UserProfile.objects.get(user_id=user_id)
                profile.status = 'approved'
                profile.save()
                messages.success(request, f"User {profile.user.username} approved successfully")
            except UserProfile.DoesNotExist:
                messages.error(request, f"User with ID {user_id} does not exist!")
            except Exception as e:
                messages.error(request, f"Error approving user {user_id}: {str(e)}")
        return redirect('approve-users')
    return render(request, 'main/approve_user.html', {'profiles': pending_profiles})
        
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
    
def manager_dashboard(request):
    return render(request, 'manager/dashboard.html')

def supervisor_dashboard(request):
    return render(request, 'supervisor/dashboard.html')

def customer_dashboard(request):
    return render(request, 'customer/dashboard.html')

def main_dashboard(request):
    return render(request, 'main/dashboard.html')

    # - User Logout

def user_logout(request):

    auth.logout(request)

    return redirect("my-login")

        