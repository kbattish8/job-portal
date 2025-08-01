from django.db import models
from candidate.models import Candidate
from recruiter.models import Job

# Create your models here.
class JobApplication(models.Model):
    class Status(models.TextChoices):
        APPLIED= 'applied','Applied'
        VIEWED= 'viewed','Viewed'
        SHORTLISTED= 'shortlisted','Shortlisted'
        REJECTED= 'rejected','Rejected'
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="applications")
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE,related_name="applications")
    applied_at=models.DateTimeField(auto_now_add= True)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.APPLIED)
    class Meta:
        unique_together = ('job','candidate')
    def __str__(self):
        return f"{self.candidate.user.username} -> {self.job.title} ({self.status})"