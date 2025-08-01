# from rest_framework.authtoken.models import Token
from django.contrib import admin


from recruiter.models import Recruiter

from .models import   Job
# admin.site.register(Token)

admin.site.register(Recruiter)

admin.site.register(Job)
