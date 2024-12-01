from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(ReservationHistory)
admin.site.register(HomeVisit)
admin.site.register(Reservation)
admin.site.register(PackageService)
admin.site.register(Package)
admin.site.register(PatientCondition)
admin.site.register(PatientHistory)
admin.site.register(Service)
admin.site.register(PackageType)
admin.site.register(patient)
admin.site.register(Administrator)
admin.site.register(Doctoravailability)
admin.site.register(DoctorSpecialization)
admin.site.register(GroupPermission)
admin.site.register(Schedule)
admin.site.register(Days)
admin.site.register(Clinic)
admin.site.register(Organization)