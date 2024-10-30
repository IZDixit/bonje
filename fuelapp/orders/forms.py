from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from .models import UserProfile,Order

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

# Customer, Placing order form.
class CreateRecordForm(forms.ModelForm):

    class Meta:

        model = Order
        fields = ['product_name','quantity','vehicle_number','driver_name','driver_id_number']

# Customer, Update order form.
class UpdateRecordForm(forms.ModelForm):

    class Meta:

        model = Order
        fields = ['product_name','quantity','vehicle_number','driver_name','driver_id_number']