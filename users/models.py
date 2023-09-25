from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, default="general doctor")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class DailyTimeSlots(models.Model):
    daily_timeslots_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    time_slots = models.JSONField()

    def __str__(self):
        return f"{self.appointment_date} - {self.doctor.doctor_name} Time Slots"


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.patient_name  # You can customize the string representation


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=100)
    appointment_purpose = models.TextField()
    availability = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment ID: {self.appointment_id} - {self.doctor.doctor_name} with {self.patient.patient_name}"
