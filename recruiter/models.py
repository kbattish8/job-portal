from django.db import models
from django.conf import settings
from company.models import CompanyProfile

#------------------- Skills --------------------------

class Skills(models.Model):
    name = models.CharField(unique = True)
    def __str__(self):
        return self.name

#------------------- Recruiter --------------------------
class Recruiter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # skills = models.ManyToManyField(Skills, blank=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, null=True, blank=True)
    position_title = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.company.name if self.company else 'No Company'}"



#------------------- JOB --------------------------

class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    jobskills = models.ManyToManyField(Skills, blank=True)  # <-- Add this
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

