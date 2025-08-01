from django.urls import path
from .views import SelectUserRoleView, SignupAPIView, LoginUserAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('set-role/', SelectUserRoleView.as_view(), name='set-role'),
]
