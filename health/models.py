from django.db import models
from registration.models import CustomUser

# Create your models here.
class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    custom_user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.doctor_name

class DailyTimeSlots(models.Model):
    doctor = models.ForeignKey(Doctor, null=True, blank=True, on_delete=models.CASCADE)
    available_date = models.DateTimeField()
    time_slots = models.JSONField()

    def __str__(self):
        return f"{self.time_slots} {self.available_date} {self.time_slots}"

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.patient_name}"

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_purpose = models.TextField(blank=True)

    def __str__(self):
        return f"{self.doctor} {self.patient}"








