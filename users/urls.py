from django.urls import path
from . import views as users_views


urlpatterns = [
    path(r'doctors/timeslots', users_views.timeslots, name='timeslots'),
    path(r'doctors/<int:doctor_id>/timeslots/', users_views.DailyTimeSlotsCombinedView.as_view(), name='daily_timeslots_combined'),
    path(r'doctors/<int:doctor_id>/timeslots/<int:timeslot_id>/edit/', users_views.DailyTimeSlotsCombinedView.as_view(), name='daily_timeslots_edit'),
    path(r'doctors/<int:doctor_id>/timeslots/<int:timeslot_id>/delete/', users_views.delete_timeslot, name='daily_timeslots_delete'),
    path(r'doctors/<int:doctor_id>/timeslots/create/', users_views.DailyTimeSlotsCombinedView.as_view(), name='daily_timeslots_create'),
    path(r'appointment/', users_views.doctor_appointments, name='appointment_detail'),
    path(r'confirm_appointment/<int:appointment_id>/', users_views.confirm_appointment, name='confirm_appointment'),
    path(r'cancel_appointment/<int:appointment_id>/', users_views.cancel_appointment, name='cancel_appointment')
    ]