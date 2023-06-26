from django.urls import path
from users.views import *

app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('consultations/<int:id>/', ConsultationListView.as_view(), name='consultation-list'),
    path('schedule/', ScheduleView.as_view(), name='consultation-list'),
    path('data/<int:id>/',get_patient_data, name='consultation-list'),
    path('register/',PatientRegisterView.as_view(), name='register'),
    path('consultationsPatient/<int:id>/',ConsultationPatient.as_view(), name='consultations-patient'),
    path('doctors/',DoctorsListView.as_view(), name='consultations-patient'),
    path('consulter/',CreateConsultationView.as_view(), name='creer-consultations'),
    path('schedules/<int:doctor_id>/',GetSchedules.as_view(), name='schedule-doctor'),
    path('description/<int:id>/',AddDescription.as_view(), name='Description-doctor'),
    path('delete/<int:consultation_id>/',delete_consultation, name='Delete-consultation'),

]
