from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from registration.models import CustomUser
from health.models import Patient, DailyTimeSlots, Doctor
from health.models import Appointment
from django.db import connection


def login_view(request):
    error_message = None
    msg = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            msg = f"Welcome {user}, Logged in successfully !!!"  # Set the message before the redirect
            return redirect('dashboard')  # Assuming you have a 'dashboard' URL pattern
        else:
            error_message = "Please enter the correct email and password"
            messages.error(request, "Please enter the correct email and password")  # Add this line to send an error message
    return render(request, 'login.html', {'error_message': error_message, "msg": msg})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successfully!')
    return redirect('login')  # Redirect to the login page after logout

def dashboard(request):
    user = request.user
    dt = Doctor.objects.filter(custom_user=user)
    ts = DailyTimeSlots.objects.filter(doctor=dt.first())
    aps = Appointment.objects.filter(doctor=dt.first())
    
    ps = [ap.patient for ap in aps]

    return render(request, 
        'dashboard.html',
        context={"user": user, "appointments": aps, "patients": ps, "doctors": dt, "time_slots": ts}
    )