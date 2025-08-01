from django.urls import path

from recruiter.views import RecruiterProfileAPIView
from company.views import CompanyProfileManageAPIView,CompanyJobDetailUpdateAPIView,CompanyJobListAPIView

 
urlpatterns = [
    path('my-jobs/', CompanyJobListAPIView.as_view(), name='job-update'),
    path('jobs/<int:pk>/', CompanyJobDetailUpdateAPIView.as_view(), name='job-detail'),
    path('recruiter/me/', RecruiterProfileAPIView.as_view(), name='recruiter-profile'),
    path('me/', CompanyProfileManageAPIView.as_view(), name='company-manage'),  # GET, PUT
]