
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserView, UsersViewsetWithFilterView, AdditionalInfoViewsetWithFilterView, MyProfileViewSet, VerifyUserEmailView, LoginUserView, TestAuthenticatedUserView, PasswordResetView, PasswordResetConfirmView, SetNewPasswordView

# app_name = 'userprofile'  
router = DefaultRouter()
router.register(r'users', UsersViewsetWithFilterView, basename='users')
router.register(r'additional', AdditionalInfoViewsetWithFilterView, basename='additional')
router.register(r'profile', MyProfileViewSet, basename='profile')

urlpatterns = [
path('register/', RegisterUserView.as_view(), name='register'),
path('verify-email/', VerifyUserEmailView.as_view(), name='verify-email'),
path('login/', LoginUserView.as_view(), name='login'),
path('test/', TestAuthenticatedUserView.as_view(), name='test'),
path('reset-pass/', PasswordResetView.as_view(), name='reset-pass'),
path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
path('', include(router.urls)),
]

