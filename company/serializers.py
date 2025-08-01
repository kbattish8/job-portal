from rest_framework import serializers

from recruiter.models import Recruiter
from company.models import CompanyProfile
from django.core.exceptions import ValidationError



#------------------------------Company----------------------------------------


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['id', 'name', 'website', 'description', 'industry', 'location', 'created_at']
        read_only_fields = ['id', 'created_at']



class RecruiterSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ['id', 'user', 'position_title', 'phone_no', 'joined_at']

class CompanyProfileDetailSerializer(serializers.ModelSerializer):
    recruiters = RecruiterSimpleSerializer(source='recruiter_set', many=True, read_only=True)

    class Meta:
        model = CompanyProfile
        fields = ['id', 'name', 'website', 'description', 'industry', 'location', 'created_at', 'recruiters']
        read_only_fields = ['id', 'created_at']