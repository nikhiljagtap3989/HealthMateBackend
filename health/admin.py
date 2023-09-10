from django.contrib import admin
from health.models import Doctor, DailyTimeSlots, Patient, Appointment

admin.site.register(Doctor)
admin.site.register(DailyTimeSlots)
admin.site.register(Patient)
admin.site.register(Appointment)
