from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput())
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput())
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())
    email = forms.EmailField(required=True,
                             widget=forms.TextInput())
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100,
                                    required=True,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                                    required=True,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1930, 2022), ))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['birthday', 'phone', 'country',
                  'city', 'address', 'bio', 'avatar']
# class ChangePasswordForm(forms.ModelForm):
#     old_password = forms.CharField(widget=forms.PasswordInput(
#         attrs={'class': 'form-control'}))
#     new_password = forms.CharField(widget=forms.PasswordInput(
#         attrs={'class': 'form-control'}))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(
#         attrs={'class': 'form-control'}))
    
    # class Meta:
    #     model = User
    #     fields = ['old_password', 'new_password', 'confirm_password']