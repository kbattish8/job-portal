from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # App routes
    path('api/', include('recruiter.urls')),
    path('api/accounts/', include('accounts.urls')), 
    path('api/company/', include('company.urls')),
    path('api/candidate/', include('candidate.urls')),

    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='jwt_token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='jwt_token_refresh'),
]
