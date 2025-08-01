from django.apps import AppConfig
import sys
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    def ready(self):
        
        if 'makemigrations' in sys.argv or 'migrate' in sys.argv or 'collectstatic' in sys.argv or 'shell' in sys.argv:
            return

        from django.contrib.auth.models import Group
        roles = ['company', 'recruiter', 'jobseeker']
        for role in roles:
            Group.objects.get_or_create(name=role)
