from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from .managers import MyUserManager

# Create your models here.
# PermissionMixin - gives us is_superuser fields, and also useful for role based access, single user access definition
class MyUser(AbstractBaseUser, PermissionsMixin):
    # fields
    # password field inherited from abstract base user class
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # custom manager object
    objects = MyUserManager()

    # username field
    USERNAME_FIELD = 'email'

    # required fields
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # some str functions or any other functions
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    # can also define - get_full_name and get_short_name but are optional