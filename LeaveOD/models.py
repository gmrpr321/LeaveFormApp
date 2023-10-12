from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
import django

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("user name must be set")

        user: User = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        # extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("super user should be a staff user")
        
        if  extra_fields.get('is_superuser') is not True:
            raise ValueError(" is super user should be a true")
        return self.create_user(username=username, password=password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    date_of_joining = models.DateField(null=True)
    # staff should select True for this field
    is_staff = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    # students should enter their mentor and class incharge ids as referrence
    mentor = models.CharField(max_length=30, null=True)
    class_incharge = models.CharField(max_length=30, null=True)
    # students should be assigned HOD according to their department
    HOD = models.CharField(max_length=30)

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "is_staff"]

    def __str__(self):
        return "username:" + self.username + " name:" + self.name 


class Form(models.Model):

    current_date = django.utils.timezone.now

    attendance_choice = (("LEAVE", "LEAVE"), ("ON DUTY", "ON DUTY"))
    student = models.ForeignKey(User, on_delete=models.CASCADE) # it means the user name of the student user
    
    year_of_study = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    date_from = models.DateField(blank=True,default=current_date)
    date_to = models.DateField(blank=True,default=current_date)
    section = models.CharField(max_length=2)
    student_name = models.CharField(max_length=100, null=True) # !!!!!!
    student_dept = models.CharField(max_length=30, null=True) # !!!!!!
    # resason should be added for both od and leave
    parent_ph_no = models.CharField(max_length=10)
    attendance_status = models.CharField(choices=attendance_choice, max_length=20)
    # here the default value of parent , staff , hod confirmation is False it is used to validate the form whether the confirmattion is given or not to proceed to next step
    parent_consent = models.BooleanField(default=False)
    staff_confirmation = models.BooleanField(default=False)
    HOD_confirmation = models.BooleanField(default = False)
