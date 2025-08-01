from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from company.models import CompanyProfile
from recruiter.models import Job, Recruiter
from recruiter.serializers import JobSerializer
from company.serializers import CompanyProfileSerializer


# ------------------------------ Permissions ----------------------------------------

class IsRecruiter(permissions.BasePermission):
    """Allow access only to recruiters."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'recruiter'


class IsCompany(permissions.BasePermission):
    """Allow access only to companies."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'company'


# ------------------------------ Company Manage ----------------------------------------

class CompanyProfileManageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCompany]

    def get(self, request):
        company = get_object_or_404(CompanyProfile, user=request.user)
        serializer = CompanyProfileSerializer(company)
        return Response(serializer.data)

    def put(self, request):
        company = get_object_or_404(CompanyProfile, user=request.user)
        serializer = CompanyProfileSerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------ Company Profile for Recruiter ----------------------------------------

class CompanyProfileDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        recruiter = get_object_or_404(Recruiter, user=request.user)
        if not recruiter.company:
            return Response({'error': 'No company assigned to this recruiter.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanyProfileSerializer(recruiter.company)
        return Response(serializer.data)

    def put(self, request):
        return Response({"error": "Recruiters are not allowed to update company details."},
                        status=status.HTTP_403_FORBIDDEN)


# ------------------------------ Company Jobs List ----------------------------------------

class CompanyJobListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCompany]

    def get(self, request):
        company = request.user.companyprofile
        jobs = Job.objects.filter(company=company).order_by('-created_at')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


# ------------------------------ Company Job Detail / Update ----------------------------------------

class CompanyJobDetailUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCompany]

    def get(self, request, pk):
        job = get_object_or_404(Job, id=pk, company=request.user.companyprofile)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def patch(self, request, pk):
        job = get_object_or_404(Job, id=pk, company=request.user.companyprofile)
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
