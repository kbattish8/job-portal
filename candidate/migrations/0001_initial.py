# Generated by Django 5.2.4 on 2025-08-01 05:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recruiter', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('bio', models.TextField(blank=True, null=True)),
                ('experience', models.PositiveIntegerField(blank=True, help_text='Experience in years', null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('skills', models.ManyToManyField(blank=True, to='recruiter.skills')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
