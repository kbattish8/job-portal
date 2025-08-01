from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from celery import shared_task
from chat.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from candidate.tasks import send_application_notification
from applications.models import JobApplication
from applications.serializers import RecruiterJobApplicationSerializer
from .models import Job, Recruiter
from .serializers import RecruiterSerializer, JobSerializer


# ------------------------------Permissions----------------------------------------
class IsRecruiter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'recruiter'


class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'company'


# ------------------------------IndexView----------------------------------------
class IndexAPIVIEW(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to the Recruiter API!',
            'endpoints': {
                'List/Create Jobs': '/api/jobs/',
                'Retrieve/Update/Delete Job': '/api/jobs/<id>/',
            }
        })


# ------------------------------Recruiter Profile----------------------------------------
class RecruiterProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        recruiter = get_object_or_404(Recruiter, user=request.user)
        serializer = RecruiterSerializer(recruiter)
        return Response(serializer.data)

    def patch(self, request):
        recruiter = get_object_or_404(Recruiter, user=request.user)
        data = request.data.copy()

        # Prevent company updates
        data.pop('company', None)

        serializer = RecruiterSerializer(recruiter, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------Job----------------------------------------
class JobListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get(self, request):
        recruiter = get_object_or_404(Recruiter, user=request.user)
        jobs = Job.objects.filter(recruiter=recruiter)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        recruiter = get_object_or_404(Recruiter, user=request.user)
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recruiter=recruiter, company=recruiter.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_object(self, pk, user):
        return Job.objects.filter(pk=pk, recruiter=user.recruiter).first()

    def get(self, request, pk):
        job = self.get_object(pk, request.user)
        if not job:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk, request.user)
        if not job:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        job = self.get_object(pk, request.user)
        if not job:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = self.get_object(pk, request.user)
        if not job:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------Job Applications----------------------------
class JobApplicationsListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get(self, request, job_id):
        recruiter = get_object_or_404(Recruiter, user=request.user)
        job = get_object_or_404(Job, id=job_id, recruiter=recruiter)
        applications = JobApplication.objects.filter(job=job)
        serializer = RecruiterJobApplicationSerializer(applications, many=True)
        return Response(serializer.data)



class UpdateApplicationStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def patch(self, request, application_id):
        application = get_object_or_404(JobApplication, id=application_id)

        # Ensure recruiter belongs to same company
        if application.job.company != request.user.recruiter.company:
            return Response(
                {'detail': 'Unauthorized to update this application.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RecruiterJobApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # --- Send notification to candidate ---
            candidate_user = application.candidate.user
            message = f"Your application for '{application.job.title}' was updated to: {application.status}."
            send_application_notification.delay(
                recipient_id=candidate_user.id,
                message=message,
                sender_id=request.user.id
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)