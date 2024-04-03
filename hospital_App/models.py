# models.pyGroup
from django.contrib.auth.models import AbstractUser,Group, Permission, User
from django.db import models
# import uuid

# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('receptionist', 'Receptionist'),
        ('patient', 'Patient'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    def __str__(self):
        return self.username

class Doctors(models.Model):
    # doctors_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctors_id = models.CharField(max_length=20)
    doctorName = models.CharField(max_length=20)
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(auto_now=False)
    availableTimeDate = models.DateTimeField(auto_now=False)
    endTimeDate = models.DateTimeField(auto_now=False)
    mobile = models.IntegerField()
    specialization = models.CharField(max_length=25)

    def __str__(self):
        return self.doctorName + ' ' + self.specialization
    

class Nurses(models.Model):
    # nurses_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nurses_id = models.CharField(max_length=20)
    nursesName = models.CharField(max_length=20)
    specialization = models.CharField(max_length=25)
    mobile = models.IntegerField()
    availableTimeDate = models.DateTimeField(auto_now=False)
    endTimeDate = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.nursesName + ' ' + self.specialization

class Patient(models.Model):
    # name= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name= models.CharField(max_length=20)
    mobile = models.IntegerField()
    medical_issue = models.CharField(max_length=30)
    doj = models.DateField()
    doe =models.DateField()

    def __str__(self):
        return self.medical_issue
    
class receptionist(models.Model):
    name= models.CharField(max_length=30)
    mobile = models.IntegerField()
    availableTimeDate = models.DateTimeField(auto_now=False)
    endTimeDate = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.name


class Token(models.Model):
    # username = models.ForeignKey(Patient, on_delete=models.CASCADE,default=None)
    username = models.CharField(max_length=30)
    age = models.IntegerField()
    number = models.IntegerField()
    adhar = models.IntegerField(default =0, blank=False, null=False)
    gender = models.CharField(max_length=10)
    disease = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    password = models.CharField(max_length=30, default =0)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user=models.OneToOneField(User,   on_delete=models.CASCADE,related_name="profile")
    phone_number=models.CharField(max_length=15)
    otp=models.CharField(max_length=100,null=True,blank=True)
    # uid=models.CharField(default=f'{uuid.uuid4}',max_length=200)

    def __str__(self):
        return self.user.username
    
class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True)
    date_issued = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.patient.name

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice.patient.name