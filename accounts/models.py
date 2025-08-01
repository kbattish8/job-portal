from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('company', 'Company'),
        ('recruiter', 'Recruiter'),
        ('candidate', 'Candidate'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

   
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # User role
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    # Status fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)  # When user signed up

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    # Optional: Used for displaying names in admin, chat, notifications
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def get_short_name(self):
        return self.first_name or self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
