from django.urls import path
from candidate.views import CandidateJobDetailView, CandidateProfileAPIView, CandidateJobListView, ApplyToJobsAPIView


 
urlpatterns = [
    path('profile/', CandidateProfileAPIView.as_view(), name='candidate-profile'),
    path('jobs/', CandidateJobListView.as_view(), name='candidate-job-list'),
    path('job/<int:id>/', CandidateJobDetailView.as_view(), name='candidate-job-detail'),
    path('jobs/<int:job_id>/apply/', ApplyToJobsAPIView.as_view(), name='apply-to-job'),
]