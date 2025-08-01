from rest_framework import serializers
from recruiter.models import  Recruiter, Job, Skills
from company.models import CompanyProfile

#------------------------------Skills----------------------------------------

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id','name']

#------------------------------Recruiter----------------------------------------

class RecruiterSerializer(serializers.ModelSerializer):
    # skills = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Recruiter
        fields = ['id', 'user', 'company', 'position_title', 'phone_no', 'joined_at']
        read_only_fields = ['id', 'joined_at', 'user']
        extra_kwargs = {
            'company': {'required': False, 'allow_null': True},
        }

    def validate_company(self, value):
        if value and not CompanyProfile.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Selected company does not exist.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

#------------------------------JOB----------------------------------------


class JobSerializer(serializers.ModelSerializer):
    skills = serializers.CharField(write_only=True, required=False)  # comma-separated input
    skill_names = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True,
        source='jobskills'
    )

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'salary', 'is_active', 'created_at', 'skills', 'skill_names']
        read_only_fields = ['id', 'created_at', 'skill_names']

    def create(self, validated_data):
        skills_str = validated_data.pop('skills', '')
        job = Job.objects.create(**validated_data)

        if skills_str:
            skill_names = [skill.strip() for skill in skills_str.split(',') if skill.strip()]
            skill_objs = []
            for name in skill_names:
                skill, _ = Skills.objects.get_or_create(name=name)
                skill_objs.append(skill)
            job.jobskills.set(skill_objs)

        return job

    def update(self, instance, validated_data):
        skills_str = validated_data.pop('skills', '')
        instance = super().update(instance, validated_data)

        if skills_str:
            skill_names = [skill.strip() for skill in skills_str.split(',') if skill.strip()]
            skill_objs = []
            for name in skill_names:
                skill, _ = Skills.objects.get_or_create(name=name)
                skill_objs.append(skill)
            instance.jobskills.set(skill_objs)

        return instance
