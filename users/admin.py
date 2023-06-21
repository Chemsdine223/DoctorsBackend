from django.contrib import admin
from users.models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Specialite)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Consultations)
admin.site.register(Schedule)
