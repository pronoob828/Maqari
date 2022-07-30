from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from maqari.models import *

# Create your models here.
class Role(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("users must have an email adress")
        if not username:
            raise ValueError("users must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username , password):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password,
            username= username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class Account(AbstractBaseUser,PermissionsMixin):

    Genders=[
        ("Male","Male"),
        ("Female","Female")
    ]

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=False)
    last_name = models.CharField(max_length=25)
    gender = models.CharField(max_length=7,choices=Genders,default = "Male")
    phone_num = PhoneNumberField(blank=True)
    current_residence = CountryField(null =True , blank = True)
    nationality = CountryField(null =True , blank = True)
    
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    is_active = models.BooleanField(default=True)

    # For staff members
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    years_of_experience = models.IntegerField(blank=True ,null = True)
    qualifications = models.TextField(max_length=500,blank=True ,null=True)
    profile_image = models.URLField(default="https://www.freeiconspng.com/thumbs/account-icon/account-icon-33.png")
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        'username',
    ]

    objects = MyAccountManager()

    def __str__(self):
        return f"{self.username} {self.last_name}"

    def serialize(self):
        
        if self.years_of_experience:
            exp = self.years_of_experience
        else:
            exp = ""
        
        return {
            'id' : self.id,
            'email' : self.email,
            'username' : self.username,
            'last_name' : self.last_name,
            'gender' : self.gender,
            'phone_num' : self.phone_num,
            'current_residence' : self.current_residence,
            'nationality' : self.nationality,
            'date_joined' : self.date_joined,
            'years_of_experience' : exp,
            'qualifications' : self.qualifications,
            'profile_image' : self.profile_image,
            'groups' : [group.name for group in self.groups.all()]
        }
