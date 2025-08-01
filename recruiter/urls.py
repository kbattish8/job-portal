from django.urls import path

from company.views import CompanyProfileDetailAPIView
from .views import ( JobApplicationsListAPIView, JobListCreateAPIView, JobDetailAPIView, IndexAPIVIEW,  RecruiterProfileAPIView, UpdateApplicationStatusAPIView )

 
urlpatterns = [
    path('', IndexAPIVIEW.as_view(), name='index'),
    path('jobs/', JobListCreateAPIView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailAPIView.as_view(), name='job-detail'),
    path('recruiter/me/', RecruiterProfileAPIView.as_view(), name='recruiter-profile'),
    path('companies/detail/', CompanyProfileDetailAPIView.as_view(), name='company-detail'),  # For recruiters
    path('jobs/<int:job_id>/applications/', JobApplicationsListAPIView.as_view(), name='job-applications-list'),
    path('applications/<int:application_id>/status/', UpdateApplicationStatusAPIView.as_view(), name='update-application-status'),  
]