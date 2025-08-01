from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from candidate.models import Candidate
from company.models import CompanyProfile
from recruiter.models import Recruiter

from .serializers import SignUpSerializer, LoginSerializer


# ---------------------- SIGNUP ----------------------
class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------- LOGIN ----------------------
class LoginUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# ---------------------- SELECT ROLE ----------------------
class SelectUserRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        role = request.data.get("role")
        user = request.user
        user.groups.clear()

        if role == "company":
            user.role = "company"
            user.save()
            group, _ = Group.objects.get_or_create(name="company")
            user.groups.add(group)
            CompanyProfile.objects.create(user=user)
            return Response({"msg": "Company role set and profile created."}, status=status.HTTP_201_CREATED)

        elif role == "recruiter":
            company_id = request.data.get("company_id")
            if not company_id:
                return Response({"error": "Company ID is required for recruiter role."}, status=status.HTTP_400_BAD_REQUEST)
            company = get_object_or_404(CompanyProfile, id=company_id)
            user.role = "recruiter"
            user.save()
            group, _ = Group.objects.get_or_create(name="recruiter")
            user.groups.add(group)
            Recruiter.objects.create(user=user, company=company)
            return Response({"msg": "Recruiter role set and linked to company."}, status=status.HTTP_201_CREATED)

        elif role == "candidate":
            user.role = "candidate"
            user.save()
            group, _ = Group.objects.get_or_create(name="candidate")
            user.groups.add(group)
            Candidate.objects.create(user=user)
            return Response({"msg": "Candidate role set."}, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid role. Choose 'company', 'recruiter', or 'candidate'."}, status=status.HTTP_400_BAD_REQUEST)
