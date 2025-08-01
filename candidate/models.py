from django.db import models
from django.conf import settings

from recruiter.models import Skills

# Create your models here.


class Candidate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Optional profile fields (you can expand as needed)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    experience = models.PositiveIntegerField(blank=True, null=True, help_text="Experience in years")
    skills = models.ManyToManyField(Skills, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Candidate: {self.user.username}"


