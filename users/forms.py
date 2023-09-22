from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DailyTimeSlots


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required = True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    first_name = forms.CharField(
        max_length=100,
        required = True,
        help_text='Enter First Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        max_length=100,
        required = True,
        help_text='Enter Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    username = forms.CharField(
        max_length=200,
        required = True,
        help_text='Enter Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password1 = forms.CharField(
        help_text='Enter Password',
        required = True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        required = True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )
    check = forms.BooleanField(required = True)
    specialization = forms.CharField(  # Add specialization field
        max_length=100,
        required=True,
        help_text='Enter Specialization',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specialization'}),
    )


    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'check',
            'specialization'
        ]


class DailyTimeSlotsForm(forms.ModelForm):
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = DailyTimeSlots
        fields = ['appointment_date', 'time_slots']

    # You can add custom validation or widgets here if needed
