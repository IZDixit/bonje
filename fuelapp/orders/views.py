from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm
from django.contrib import messages
# Create your views here.

def home(request):

    return render(request, 'main/index.html')

# - Register a User (according to youtube)
# def register(request):
    
#     form = CreateUserForm()

#     if request.method == "POST":

#         form = CreateUserForm(request.POST)

#         if form.is_valid():

#             user = form.save() # using the user variable will trigger the signals.py to create UserProfile.

#             messages.success(request, "Account created successfully!")

#             return redirect("my-login")
        
#         else:

#             messages.error(request, 'There was ana error in the form submission.')
        
#     context = {'form': form}
#     return render(request, 'main/register.html', context=context)
    

# - Register a User
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # We will login the user automatically
            return redirect('dashboard')
    else:
        form = CreateUserForm()
    context = {'form':form}
    return render(request, 'main/register.html', context=context)
        

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

                auth.login(request, user)

                # return redirect("dashboard")
            
    context = {'form':form}

    return render(request, 'main/my-login.html', context=context)


@login_required(login_url='my-login')
def dashboard(request):
    if request.user.is_authenticated:
        user_type = request.user.userprofile.user_type

        #Determine which template to use based on user type
        if user_type == 'manager':
            return render(request, 'manager/dashboard.html')
        elif user_type == 'supervisor':
            return render(request, 'supervisor/dashboard.html')
        elif user_type == 'Customer':
            return render(request, 'customer/dashboard.html')
        else:
            return render(request, 'main/dashboard.html') # Default Template
    else:
        return redirect('my-login')

    # - User Logout

def user_logout(request):

    auth.logout(request)

    return redirect("my-login")