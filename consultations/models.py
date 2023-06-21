# from django.conf import settings
# from django.db import models


# from users.models import Doctor, Patient

# # Create your models here.


# class Specialite(models.Model):   
#     nom = models.CharField(max_length=20, blank=True, null=True)

# class Consultations(models.Model):
#     # doctor = models.ForeignKey(get_user_model(), related_name='doctor_appointments', on_delete=models.CASCADE)
#     # patient = models.ForeignKey(get_user_model(), related_name='patient_appointments', on_delete=models.CASCADE)
    
#     doctor_id = models.ForeignKey(Doctor, on_delete= models.CASCADE, blank=True)
#     patient_id = models.ForeignKey(Patient, on_delete= models.CASCADE, blank=True)
#     specialite = models.ForeignKey(Specialite, on_delete= models.CASCADE, blank=True)
#     date_de_consultation = models.TimeField(blank=True)
    

