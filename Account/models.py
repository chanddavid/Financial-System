from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token
import random, string


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None, **other_fields):
        email = self.normalize_email(email)
        user  = self.model(email=email, username=username, **other_fields)
        if password is None:
            S = 10 
            password=''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
        user.set_password(password)
        user.save()
        Token.objects.get_or_create(user=user)
        return user
    
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is False:
            raise ValueError('Superuser must be assigned is_staff = True')

        if other_fields.get('is_superuser') is False:
            raise ValueError('Superuser must be assigned is_superuser = True')
       
        return self.create_user(email=email, username=username, password=password, **other_fields)
        

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', unique=True)
    username = models.CharField(verbose_name='Username',max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    citizenship_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.JSONField(blank=True, null=True)  
    is_active = models.BooleanField(verbose_name='Active',default=True)
    is_staff  = models.BooleanField(verbose_name='Staff',default=False)
    is_supervisor= models.BooleanField(verbose_name='Supervisor',default=False)
    is_superuser = models.BooleanField(verbose_name='Superuser',default=False)
    date_joined = models.DateField(verbose_name='date joined',auto_now_add=True,auto_now=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomAccountManager()

    def __str__(self):
        return f'{self.email}'
    
    
    class Meta:
        db_table='User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'