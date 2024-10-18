from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from .models import UserProfile

class CreateUserForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password','user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # N/b Added later (next steps)
            # Create UserProfile with 'pending' status
            UserProfile.objects.create(user=user, user_type=self.cleaned_data['user_type'])
        return user

    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))

    # def confirm_login_allowed(self, user):
    #     # Block certain user types from logging into unauthorized page.
    #     print(f"User: {user.username}, User Type: {user.userprofile.user_type}")  # Debugging line
    #     if hasattr(user, 'userprofile') and user.userprofile.user_type == 'customer':
    #         raise forms.ValidationError("Customers are not allowed to log in here.")







# First comment out
# class CreateUserForm(UserCreationForm):
#     USER_TYPE_CHOICES = (
#         ('manager', 'Manager'),
#         ('supervisor', 'Supervisor'),
#         ('customer', 'Customer'),
#     )

#     user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label="User Type")
#     phone = forms.CharField(max_length=15, required=False, label="Phone")

#     class Meta:
#         model = User
#         fields = ['username', 'password1', 'password2']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#             # Create the associated User Profile with the chosen user type and phone
#             user_type = self.cleaned_data['user_type']
#             phone = self.cleaned_data['phone']
#             UserProfile.objects.create(user=user, user_type=user_type, phone=phone)
#         return user