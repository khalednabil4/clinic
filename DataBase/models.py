import datetime

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *
import random
from mptt.models import MPTTModel, TreeForeignKey
import string

DAY_CHOICES = [
    ("MONDAY", 'Monday'),
    ("TUESDAY", 'Tuesday'),
    ("WEDNESDAY", 'Wednesday'),
    ("THURSDAY", 'Thursday'),
    ("FRIDAY", 'Friday'),
    ("SATURDAY", 'Saturday'),
    ("SUNDAY", 'Sunday'),
]
def generate_unique_code():
    # Generate a random string of length 8 (you can adjust the length and characters)
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
class Organization(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    def __str__(self):
        return str(self.name)
class Clinic(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    code=models.CharField(max_length=50)
    IsAvailable=models.BooleanField(default=1)
    AvaiableTimeFrom=models.DateField(blank=True,null=True)
    AvaiableTimeTo=models.DateField(blank=True,null=True)
    DoctorSpecialization = models.ForeignKey('DoctorSpecialization', related_name='Clinic', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.name)
class Days(models.Model):

    name = models.CharField(max_length=20, choices=DAY_CHOICES)
    Admin=models.ForeignKey('Administrator', related_name='DaysOpen',on_delete=models.CASCADE)
    date = models.DateField()
    def __str__(self):
        return f"{self.name} - {self.date}"
class Schedule(models.Model):
    Doctoravailability = models.ForeignKey('Doctoravailability', on_delete=models.CASCADE, related_name='Schedule')
    IsCome = models.BooleanField(default=1)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='Schedule')
    AttendanceTime = models.TimeField()
    TimeStart=models.TimeField()
    TimeLeave=models.TimeField()
    LeaveTime = models.TimeField()
    def __str__(self):
        return f"{self.doctor.name} - {self.clinic.name} from {self.attendance_time} to {self.leave_time}"

class GroupPermission(Group):  # groups newly added
    group_name = models.CharField(max_length=100)
    Clinic = models.ForeignKey(Organization, related_name='groups', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.name)
class DoctorSpecialization(models.Model):
    name=models.CharField(max_length=100)
    Code=models.CharField(max_length=100)
class Doctoravailability(models.Model):
    DateFrom=models.TimeField()
    DayOpen = models.ForeignKey(Days, on_delete=models.CASCADE, related_name='Schedule')
    DateTo=models.TimeField()
    Status=models.BooleanField(default=0)
    Doctor=models.ForeignKey('Administrator', related_name='admin', on_delete=models.CASCADE)


class Administrator(User):
    name=models.CharField(max_length=100, blank=True, default="User")
    profile_img = models.ImageField(upload_to='Admins', default='/Admins/doctor.jpg')
    bio = models.CharField(max_length=100, blank=True, default="User Here")
    SpecialInformation=models.TextField(null=True,blank=True)
    GraduationFrom=models.CharField(max_length=100)
    GraduationDate = models.DateField(max_length=100)
    IsDoctor=models.BooleanField(default=0)
    Clinic = models.ManyToManyField(Clinic, related_name='administrators', blank=True,null=True)
    DoctorSpecializations = models.ManyToManyField(DoctorSpecialization, related_name='administrators', blank=True,null=True)
    group_in = models.ForeignKey(GroupPermission, related_name='admin',on_delete=models.CASCADE,default=None,null=True)
    Organization = models.ForeignKey(Organization, related_name='admin', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class patient(User):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True, blank=True, null=True)
    profile_img = models.ImageField(blank=True,null=True,upload_to='patient', default='/patient/account.png')
    Organization = models.ForeignKey(Organization, related_name='Clinic', null=True, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    @property
    def age(self):
        if self.birth_date:
            age = datetime.date.today() - self.birth_date
            return int(age.days / 365.25)
        return None  # In case birth_date is not set

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_code()  # Generate unique code
        super().save(*args, **kwargs)

class PackageType(models.Model):
    category=models.CharField(max_length=50)
    urgency_level = models.IntegerField()

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='services')
    doctor = models.ForeignKey(Administrator, on_delete=models.CASCADE, related_name='Service')
    NextTime=models.DateField()
    Immediately=models.BooleanField()
    def __str__(self):
        return f"{self.name} at {self.clinic.name} (Dr. {self.doctor.name})"
class PatientHistory(models.Model):
    DateTO=models.DateField()
    DateFrom=models.DateField()
    Doctor=models.CharField(max_length=50,blank=True,null=True)
    Doc = models.ImageField(blank=True, null=True, upload_to='PatientDoc')
    patient= models.ForeignKey(patient, on_delete=models.CASCADE, related_name='PatientHistory')
    PatientVitals=models.JSONField(null=True,blank=True)
    Note=models.TextField()


class PatientCondition(models.Model):
    PatientCase= models.TextField()
    DoctorRequirements=models.TextField()
    Service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='PatientCondition')
    PatientVitals=models.JSONField(null=True,blank=True)
    Doc = models.ImageField(blank=True, null=True, upload_to='PatientDoc')
class Package(models.Model):
    name = models.CharField(max_length=200)
    patient = models.ForeignKey(patient, related_name='Package', on_delete=models.CASCADE)
    PackageType = models.ForeignKey(PackageType, related_name='Package', on_delete=models.CASCADE)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    StartDate = models.DateField()
    EndDate = models.DateField(null=True,blank=True)
    attributes=models.JSONField()

class PackageService(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='PackageService')
    Reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE,related_name='PackageService')
    special_price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        unique_together = ['package', 'Reservation']
    def __str__(self):
        return f"{self.service.name} in {self.package.name}"

class Reservation(MPTTModel):
    patient = models.ForeignKey(patient, on_delete=models.CASCADE, related_name='reservations')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reservations')
    packageservice = models.ForeignKey(PackageService, related_name='reservations', on_delete=models.SET_NULL, null=True, blank=True)
    #reservation_date = models.DateTimeField()
    exclusivity=models.BooleanField(default=0)
    onSite=models.BooleanField(default=0)
    ReservationNumber=models.IntegerField()
    Schedule=models.ForeignKey(Schedule,related_name='Reservation', on_delete=models.SET_NULL, null=True, blank=True)
    HomeVist = models.ForeignKey('HomeVisit', related_name='reservations', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ResponseTime = models.DateTimeField(null=True, blank=True)
    Status = models.CharField(max_length=20, choices=[
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('FOLLOWUP', 'Follow-up')
    ])
    notes = models.TextField(blank=True, null=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    PaymentType = models.CharField(max_length=20, choices=[
        ('CASH', 'Cash'),
        ('CREDIT_CARD', 'Credit Card'),
        ('BANK_TRANSFER', 'Bank Transfer')
    ], default='CASH')
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2)  # Total service cost
    AmountPaid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class MPTTMeta:
        order_insertion_by = ['reservation_date']

    @property
    def final_price(self):
        if self.package_service:
            return self.package_service.special_price
        return self.service.base_price

class DoctorPaymentConfig(models.Model):
    Doctor= models.ForeignKey('Administrator', on_delete=models.CASCADE, related_name='DoctorPaymentConfig')
    Way= models.CharField(max_length=20, choices=[
        ('EveryDayCome', '='),
        ('Percentage', '%'),
        ('EveryDrRevealed', '+'),
        ('BYMonth', '*')
    ])
    TimeStart=models.DateTimeField(auto_now=True)
    TimeEnd=models.DateTimeField(blank=True,null=True)
    IsActive = models.BooleanField(default=True)
    @property
    def TotalEarnings(self):
        pass



class ChatRoom(models.Model):
    patient = models.ForeignKey('patient', on_delete=models.CASCADE, related_name='chat_rooms')
    administrator = models.ForeignKey('Administrator', on_delete=models.CASCADE, related_name='chat_rooms')
    CreatedAt = models.DateTimeField(auto_now_add=True)
    LastMessageAt = models.DateTimeField(auto_now=True)
    ISActive = models.BooleanField(default=True)
    def __str__(self):
        return f"Chat between {self.patient.name} and {self.administrator.name}"

class Message(models.Model):
    ChatRoom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='Message')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='SentMessage')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    IsRead = models.BooleanField(default=False)
    Attachment = models.FileField(upload_to='Chatattachments/', null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender.name} at {self.sent_at}"
class HomeVisit(models.Model):
    location = models.CharField(max_length=255)  # e.g., an address or description
    latitude = models.FloatField()  # Latitude for geolocation
    longitude = models.FloatField()  # Longitude for geolocation
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='HomeVisit')
    SitePrice= models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"HomeVisit for {self.reservation.patient.name} at {self.location}"



class ReservationHistory(MPTTModel):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='history')
    change_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    Details = models.TextField(blank=True, null=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return f"Change in reservation {self.reservation.id} - {self.change_type} at {self.created_at}"

