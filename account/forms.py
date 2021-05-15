from .models import BlogUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class SignupForm(UserCreationForm):
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your confirm password :', 'class': 'form-control'}))
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your  password :', 'class': 'form-control'}))

    class Meta:
        model = BlogUser
        fields = ['username', 'first_name', 'last_name',
                  'email', 'mobile_no', 'en_no', 'year', 'sem', 'gender', 'profile_image']
        labels = {'username': 'Enter Username ', 'first_name': 'Enter Your first  name',
                  'last_name': 'Enter Your last name', 'email': 'Enter Your Email', }
        widgets = {'username': forms.TextInput(
            attrs={'placeholder': 'Enter your username:', 'class': 'form-control'}),

            'first_name': forms.TextInput(
            attrs={'placeholder': 'Enter  First name :', 'class': 'form-control'}),

            'last_name': forms.TextInput(
            attrs={'placeholder': 'Enter last name :', 'class': 'form-control'}),

            'email': forms.TextInput(
            attrs={'placeholder': 'Enter your Email :', 'class': 'form-control'}),

            'mobile_no': forms.TextInput(
            attrs={'placeholder': 'Enter your Mobile Number :', 'class': 'form-control'}),

            'en_no': forms.TextInput(
            attrs={'placeholder': 'Enter your enrollment Number :', 'class': 'form-control'}),

            'profile_image': forms.FileInput(
            attrs={'placeholder': 'choose your profile image :', 'class': 'form-control'}),
        }


class EditUserProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'date_joined', 'last_login']
        labels = {'username': 'Enter Username ', 'first_name': 'Enter Your first  name',
                  'last_name': 'Enter Your last name', 'email': 'Enter Your Email', }
        exclude = ['username']
