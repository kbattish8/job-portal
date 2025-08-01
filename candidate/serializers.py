from rest_framework import serializers
from candidate.models import  Candidate
from recruiter.models import Skills



#------------------------------JOB Seeker----------------------------------------


class CandidateSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    
    class Meta:
        model = Candidate
        fields = ['full_name', 'bio', 'experience', 'location', 'skills']

    def get_skills(self, obj):
        return [skill.name for skill in obj.skills.all()]

    def update(self, instance, validated_data):
        skills_data = self.initial_data.get('skills')
        if skills_data:
            if isinstance(skills_data, str):
                skill_names = [name.strip() for name in skills_data.split(',')]
                skill_objs = []
                for name in skill_names:
                    skill_obj, created = Skills.objects.get_or_create(name__iexact=name, defaults={'name': name})
                    skill_objs.append(skill_obj)
                instance.skills.set(skill_objs)
        
        # update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



