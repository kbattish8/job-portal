from rest_framework import serializers
from applications.models import  JobApplication




#------------------------------JOB Seeker----------------------------------------


class CandidateJobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model =JobApplication
        fields = ['id','candidate','job','status','applied_at']
        read_only_fields = ['candidate','status','applied_at']

class RecruiterJobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model =JobApplication
        fields = ['id','candidate','job','status','applied_at']
        read_only_fields = ['candidate','job','applied_at']



