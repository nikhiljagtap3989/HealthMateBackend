from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import DailyTimeSlots, Doctor, Appointment
from .forms import DailyTimeSlotsForm
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import DailyTimeSlots
import json
import datetime
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user
            # Create the associated Doctor instance
            doctor_name = f"{user.first_name} {user.last_name}"
            specialization = form.cleaned_data['specialization']
            doctor = Doctor(doctor_name=doctor_name, specialization=specialization, user=user)
            doctor.save()
            messages.success(request, 'Account was created successfully.')
            return redirect('home')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form}
            return render(request, 'register.html', context)

    return render(request, 'register.html', {})

@login_required
def info(request):
    user_info = {
        'username': request.user.username,
        'email': request.user.email,
        'specialization': None  # Initialize specialization to None
    }

    try:
        # Attempt to retrieve the associated Doctor object for the logged-in user
        doctor = Doctor.objects.get(user=request.user)
        user_info['specialization'] = doctor.specialization
        user_info['doctor_id'] = doctor.doctor_id
    except Doctor.DoesNotExist:
        pass

    return render(request, 'info/profile.html', {'user_info': user_info})


@login_required
def timeslots(request):
    user = request.user
    form = DailyTimeSlotsForm(instance=None)
    doctor = Doctor.objects.get(user=request.user)
    time_slots = DailyTimeSlots.objects.filter(doctor__user=user).order_by('appointment_date')
    return render(request, 'info/daily_timeslots_combined.html', {'doctor': doctor, 'time_slots': time_slots, 'form': form})

@method_decorator(login_required, name='dispatch')
class DailyTimeSlotsCombinedView(View):
    template_name = 'info/daily_timeslots_combined.html'

    def get(self, request, doctor_id, timeslot_id=None):
        print(doctor_id)
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        time_slots = DailyTimeSlots.objects.filter(doctor=doctor)
        form = DailyTimeSlotsForm(instance=None)
        print(doctor)
        if timeslot_id:
            # If timeslot_id is provided, it means we want to edit a specific time slot
            time_slot = get_object_or_404(DailyTimeSlots, daily_timeslots_id=timeslot_id)
            form = DailyTimeSlotsForm(instance=time_slot)
        print("I am Here")
        return render(request, 'info/daily_timeslots_combined.html', {'doctor': doctor, 'time_slots': time_slots, 'form': form})

    def post(self, request, doctor_id, timeslot_id=None):
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        form = DailyTimeSlotsForm(request.POST)
        print("Updating time slots")
        if form.is_valid():
            if timeslot_id:
                # If timeslot_id is provided, it means we are updating an existing time slot
                time_slot = get_object_or_404(DailyTimeSlots, daily_timeslots_id=timeslot_id)
                form = DailyTimeSlotsForm(request.POST, instance=time_slot)
                form.save()
            else:
                # If timeslot_id is not provided, it means we are creating a new time slot
                new_time_slot = form.save(commit=False)
                new_time_slot.doctor = doctor
                new_time_slot.save()

            return redirect('daily_timeslots_combined', doctor_id=doctor_id)

        time_slots = DailyTimeSlots.objects.filter(doctor=doctor)
        return render(request, self.template_name, {'doctor': doctor, 'time_slots': time_slots, 'form': form})

@login_required
def delete_timeslot(request, doctor_id, timeslot_id):
    if request.method == "POST":
        time_slot = get_object_or_404(DailyTimeSlots, daily_timeslots_id=timeslot_id)
        time_slot.delete()
        print("deleting timslot")
        return redirect('daily_timeslots_combined', doctor_id=doctor_id)

@login_required
def doctor_appointments(request):
    user = request.user
    doctor = get_object_or_404(Doctor, user=user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('appointment_date', 'appointment_time')

    # Define the number of appointments to display per page
    appointments_per_page = 8  # You can change this number as needed

    paginator = Paginator(appointments, appointments_per_page)
    page_number = request.GET.get('page')
    page_appointments = paginator.get_page(page_number)

    context = {
        'doctor': doctor,
        'appointments': page_appointments,
    }
    return render(request, 'info/doctor_appointments.html', context)
@login_required
def confirm_appointment(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    if not appointment.availability:
        appointment.availability = True
        appointment.save()
        # Send an email to the patient
        patient = appointment.patient
        subject = 'Appointment Confirmation'
        message = f'Your appointment with {appointment.doctor.doctor_name} on {appointment.appointment_date} at {appointment.appointment_time} has been confirmed.'
        from_email = 'akolkar.pooja23@gmail.com'  # Use your email
        recipient_list = [patient.email]  # Use the patient's email
        send_mail(subject, message, from_email, recipient_list)

    return redirect('appointment_detail')

@login_required
def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    if appointment.availability:
        appointment.availability = False
        appointment.save()
    # Send an email to the patient
    patient = appointment.patient
    subject = 'Appointment Cancellation'
    message = f'Your appointment with {appointment.doctor.doctor_name} on {appointment.appointment_date} at {appointment.appointment_time} has been cancelled.'
    print("++++++", message)
    from_email = 'akolkar.pooja23@gmail.com'  # Use your email
    recipient_list = [patient.email]  # Use the patient's email
    send_mail(subject, message, from_email, recipient_list)

    return redirect('appointment_detail') 


def save_time_slots(request, doctor_id):
    if request.method == 'POST':
        selected_slots = json.loads(request.POST.get('timeslots'))
        
        # Create or update the DailyTimeSlots object
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        appointment_date = request.POST.get('appointmentdate')
        
        try:
            # Try to retrieve an existing DailyTimeSlots object
            daily_timeslot = DailyTimeSlots.objects.get(doctor=doctor, appointment_date=appointment_date)
        except DailyTimeSlots.DoesNotExist:
            # If it doesn't exist, create a new one with an empty list for time_slots
            daily_timeslot = DailyTimeSlots(doctor=doctor, appointment_date=appointment_date, time_slots=[])

        # Update the time_slots field with the selected slots
        daily_timeslot.time_slots = selected_slots
        daily_timeslot.save()
        return JsonResponse({'message': 'Time slots saved successfully'})

    return JsonResponse({'message': 'Invalid request'})
