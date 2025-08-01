from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from rest_framework import generics
from recruiter.models import Job
from recruiter.serializers import JobSerializer
from rest_framework.permissions import IsAuthenticated
from candidate.models import Candidate
from candidate.serializers import CandidateSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chat.models import Notification
from .tasks import send_application_notification
from applications.models import JobApplication
from applications.serializers import CandidateJobApplicationSerializer


#------------------------------Permisssions----------------------------------------

# Custom permission to ensure only recruiters can access certain endpoints
class IsRecruiter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'recruiter'


class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'company'


#------------------------------ Candidate ----------------------------------------


class CandidateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, user):
        try:
            return Candidate.objects.get(user=user)
        except Candidate.DoesNotExist:
            return None

    def get(self, request):
        # print(request.user.role)
        if request.user.role != 'candidate':
            return Response({"error": "You are not a Candidate."}, status=403)
        
        profile = self.get_object(request.user)
        if not profile:
            return Response({"error": "Candidate profile not found."}, status=404)
        
        serializer = CandidateSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.role != 'candidate':
            return Response({"error": "You are not a Candidate."}, status=403)
        
        profile = self.get_object(request.user)
        if not profile:
            return Response({"error": "Candidate profile not found."}, status=404)
        
        serializer = CandidateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)


#------------------listing Jobs----------------------


class CandidateJobListView(APIView):
    """
    API view for candidates to list all available jobs.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        jobs = Job.objects.all().order_by('-created_at')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#------------------Candidate JOB Details---------------
class CandidateJobDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # or allow any

    def get(self, request, id):
        try:
            job = Job.objects.get(id=id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ApplyToJobsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, job_id):
        user = request.user
        if user.role != 'candidate':
            return Response({'detail': 'Only candidates can apply.'}, status=status.HTTP_403_FORBIDDEN)

        job = get_object_or_404(Job, id=job_id)

        if JobApplication.objects.filter(candidate=user.candidate, job=job).exists():
            return Response({'detail': 'Already applied to this job.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create application
        application = JobApplication.objects.create(candidate=user.candidate, job=job)

        # Prepare message
        message = f"New application from {user.get_full_name() or user.username} for '{job.title}'."

        # Send notification asynchronously via Celery
        send_application_notification.delay(
            recipient_id=job.recruiter.user.id,
            message=message,
            from_user_id=user.id
        )

        return Response(CandidateJobApplicationSerializer(application).data, status=status.HTTP_201_CREATED)