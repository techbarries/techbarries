from django.db import models

from helpers.models import TrackingModel
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, UserManager, PermissionsMixin)


class MyUserManager(UserManager):
    def _create_user(self, email,password,username=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # if not username:
        #     raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email, username=None , password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password,username, **extra_fields)

    def create_superuser(self,  email,username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password,username, **extra_fields)

        
class User(AbstractBaseUser, PermissionsMixin,TrackingModel):
    class ProfileAccessType(models.TextChoices):
        PUBLIC = 'PUBLIC', ('PUBLIC')
        PRIVATE = 'PRIVATE', ('PRIVATE')
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        ("username"),
        max_length=150,
        unique=False,
        validators=[username_validator],
        error_messages={
            "unique":("A user with that username already exists."),
        },
        blank=True,
        null=True, default=None
    )
    uid = models.CharField(("uid"), max_length=150, blank=True)
    user_token = models.TextField(("user token"),default=None,null=True,blank=True)
    first_name = models.CharField(("first name"), max_length=150, blank=True)
    last_name = models.CharField(("last name"), max_length=150, blank=True)
    profile_picture_url = models.CharField(("profile picture url"), max_length=250, blank=True)
    profile_picture_image = models.ImageField(upload_to="profile/%Y/%m/%d/",null=True,blank=True,)
    phone_number = models.CharField(("phone number"), max_length=50, blank=True)
    date_of_birth=models.DateField(blank=True,null=True)
    job_title=models.CharField(("Job Title"), max_length=100, blank=True)
    degree_title=models.CharField(("Degree Title"), max_length=100, blank=True)
    country = models.CharField(("Country"), max_length=100, blank=True)
    university=models.ForeignKey("events.University",on_delete=models.CASCADE,related_name="university",blank=True,null=True, default=None)
    email = models.EmailField(("email address"), blank=False,unique=True)
    profile_access_type=models.CharField(max_length=10,choices=ProfileAccessType.choices,default=ProfileAccessType.PUBLIC,null=True)   

    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]

    @property
    def token(self):
        return ""

class Device(TrackingModel):
    device_name=models.CharField(max_length=255,blank=True)
    fcm_token=models.CharField(max_length=255,blank=True)
    os=models.CharField(max_length=255,blank=True) 
    user_id=models.ForeignKey(to=User,related_name="user",on_delete=models.CASCADE)      
    created_by=models.ForeignKey(to=User,related_name="created_by_user",on_delete=models.CASCADE,null=True,default=None)      

    @property
    def token(self):
        return ""

class SmsOTP(TrackingModel,models.Model):
    phone = models.IntegerField(blank=False)
    otp = models.IntegerField(null=True,blank=False)
    is_verified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, null=True,blank=False)
    def __str__(self):
            return str(self.phone)        