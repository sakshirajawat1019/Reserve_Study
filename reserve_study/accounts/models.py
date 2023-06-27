from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from organization.models import Organization


# Create your models here.
from django.contrib.auth.models import User


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name   = models.CharField(max_length=225,blank=True,null=True)
    last_name    = models.CharField(max_length=225,blank=True,null=True)
    email = models.EmailField(unique=True, max_length=255)
    phone_no = models.CharField(max_length=12, blank=True,null=True)
    company = models.CharField(max_length=225,blank=True,null=True)
    position = models.CharField(max_length=225,blank=True,null=True)
    additional_info = models.CharField(max_length=225,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    otp = models.IntegerField(blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=225,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # def __str__(self):
    #     return self.get_full_name()
    
    # def get_full_name(self):
    #     """
    #     Returns the first_name plus the last_name, with a space in between.
    #     """
    #     full_name = '%s %s' % (self.firstname, self.lastname)
    #     if full_name: return full_name.strip()
    #     else: return self.email

    # def get_short_name(self):
    #     "Returns the short name for the user."
    #     if self.firstname: return self.firstname
    #     else: return self.email

# class AccessUser(models.Model):
#     read_access_users = models.ManyToManyField(CustomUser, related_name='scenarios_with_read_access', blank=True)
#     write_access_users = models.ManyToManyField(CustomUser, related_name='scenarios_with_write_access', blank=True)

class CommunityInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser,null=True, on_delete=models.CASCADE)
    community_name = models.CharField(max_length=100, blank=True, default='demo_community')
    community_address = models.CharField(max_length=100, blank=True, default='demo')
    subscription_type = models.CharField(max_length=100, blank=True, default='Standard')
    period = models.CharField(blank=False, null=False, default="2023-2024")
    max_number_of_scenarios = models.IntegerField(blank=False, null=False, default=5)
    subscription_status = models.BooleanField(blank=False, null=False, default=True)
