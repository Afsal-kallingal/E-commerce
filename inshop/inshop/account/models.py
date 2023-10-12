from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    otp = models.CharField(max_length=6)
    address = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()  # Assign the custom manager here

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email





# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class Account(AbstractUser):
    # username = models.CharField(max_length=25,unique=True)
    # email = models.EmailField(unique=True)
    # name = models.CharField(max_length=255)
    # otp = models.CharField(max_length=6)
    # address = models.TextField(null=True)

#     # def save(self, *args, **kwargs):
#     #     if not self.pk:
#     #         self.set_password(self.password)
#     #     super(Account, self).save(*args, **kwargs)

#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = []
    
#     def __str__(self):
#         return self.username




# # class Account(AbstractUser):
# #     email=models.EmailField( unique=True)
# #     name=models.CharField(max_length=255)
# #     otp=models.CharField(max_length=6)
# #     address=models.TextField(null=True)
    
# #     def save(self, *args, **kwargs):
# #         if not self.pk: 
# #             self.set_password(self.password)
# #         super(Account, self).save(*args, **kwargs)

# #     USERNAME_FIELD = "email"
# #     REQUIRED_FIELDS = []

# #     def __str__(self):
# #         return self.email