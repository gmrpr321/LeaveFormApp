from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


# class UserManager(BaseUserManager):
#     def create_user(self, username, password, **extra_fields):
#         if not username:
#             raise ValueError("user name must be set")

#         user: User = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, username, password, **extra_fields):
#         return self.create_user(username=username, password=password, **extra_fields)


class AppUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # name = models.CharField(max_length=100)
    date_of_joining = models.DateField(null=True)
    # staff should select True for this field
    is_staff = models.BooleanField()
    is_hod = models.BooleanField()
    # students should enter thier mentor and class incharge ids as referrence
    mentor_username = models.CharField(max_length=30, null=True)
    class_incharge_username = models.CharField(max_length=30, null=True)
    # students should be assigned HOD according to their department
    HOD_username = models.CharField(max_length=30,null=True)


class Form(models.Model):
    attendance_choice = (("LEAVE", "LEAVE"), ("ON DUTY", "ON DUTY"))
    student = models.CharField(max_length=200)
    year_of_study = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    date_from = models.DateField()
    date_to = models.DateField()
    section = models.CharField(max_length=2)
    student_name = models.CharField(max_length=100, null=True)
    student_dept = models.CharField(max_length=30, null=True)
    parent_ph_no = models.CharField(max_length=10)
    attendance_status = models.CharField(choices=attendance_choice, max_length=20)
    is_parent_consent = models.BooleanField()
    is_staff_consent = models.BooleanField()
    is_HOD_consent = models.BooleanField()
