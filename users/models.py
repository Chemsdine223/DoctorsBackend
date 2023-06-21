from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

# from consultations.models import Specialite


class AccountManager(BaseUserManager):
    def create_user(self, prenom, nom, phone, password=None):
        account = self.model(prenom=prenom, nom=nom, phone=phone)
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, prenom, nom, phone, password):
        user = self.create_user(prenom, nom, phone, password)
        user.is_staff = True 
        user.is_superuser = True

        user.save(using=self._db)
        return user
    

    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    ROLES = (
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor')
    )

    phone = models.CharField(max_length=17, unique=True)
    prenom = models.CharField(max_length=20, blank=True, null=True)
    nom = models.CharField(max_length=20, blank=True, null=True)
    # nni = models.CharField(unique=True, max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLES, default='Patient') 
    
    objects = AccountManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ["prenom", "nom"]

    
    def __str__(self):
        return str(self.prenom)





class Patient(CustomUser):
    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return str(self.prenom)
    def __str__(self):
        return str(self.nom)
    

class Specialite(models.Model):   
    nom = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return str(self.nom)

class Doctor(CustomUser):
    specialite = models.ForeignKey(Specialite,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.nom)


class Consultations(models.Model):
    # doctor = models.ForeignKey(get_user_model(), related_name='doctor_appointments', on_delete=models.CASCADE)
    # patient = models.ForeignKey(get_user_model(), related_name='patient_appointments', on_delete=models.CASCADE)
    
    doctor_id = models.ForeignKey(Doctor, on_delete= models.CASCADE, blank=True)
    patient_id = models.ForeignKey(Patient, on_delete= models.CASCADE, blank=True)
    specialite = models.ForeignKey(Specialite, on_delete= models.CASCADE, blank=True)
    heure_de_consultation = models.CharField(blank=True, max_length=200)
    date_de_consultation = models.CharField(blank=True, max_length=200)
    description = models.CharField(blank=True, max_length=200)


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    lundi = models.CharField(max_length=50, default='9H - 11H')
    mardi = models.CharField(max_length=50, default='13H - 15H')
    mercredi = models.CharField(max_length=50, default='10H - 14H')
    jeudi = models.CharField(max_length=50, default='8H - 12H')
    vendredi = models.CharField(max_length=50, default='14H - 18H')
    samedi = models.CharField(max_length=50, default='9H - 12H')
    dimanche = models.CharField(max_length=50, default='Bientot')

    

