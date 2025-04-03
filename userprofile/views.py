from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import OneTimePassword, User
from .serializers import UserRegisterSerializer,MyProfileSerializer, AdditionalPersonalInfo,LoginSerializer, PasswordResetSerializer,SetNewPasswordSerializer,UserSerializer,AdditionalInfoSerializer
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    viewsets,
    filters,
    parsers,
    generics,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code_to_user(user['email'])

            return Response ({
                'data': user,
                'message': f"Thanks for signing up with this pass code",              
            },
            status=status.HTTP_201_CREATED
            )
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class VerifyUserEmailView(GenericAPIView):
#     def post(self, request):
#         otpcode = request.data.get('otp')
#         try:
#             user_code_obj = OneTimePassword.objects.get(code=otpcode)
#             user = user_code_obj.user
#             if not user.is_verified:
#                 user.is_verified=True
#                 user.save()
#                 return Response ({
#                 'message': f"Account Email verified successfully",              
#             },
#             status=status.HTTP_200_OK
#             )
#             return Response ({
#                 'message': f"Something wrong with this OTP. This OTP is used",              
#             },
#             status=status.HTTP_400_BAD_REQUEST
#             )
#         except OneTimePassword.DoesNotExist:
#             return Response ({
#                 'message': f"OPT not provided",              
#             },
#             status=status.HTTP_404_NOT_FOUND
#             )


class VerifyUserEmailView(APIView):
    def post(self, request):
        otpcode = request.data.get('otp')
        try:
            user_code_obj = OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message': "Account email verified successfully",
                }, status=status.HTTP_200_OK)

            return Response({
                'message': "This OTP has already been used.",
            }, status=status.HTTP_400_BAD_REQUEST)

        except OneTimePassword.DoesNotExist:
            return Response({
                'message': "OTP not found.",
            }, status=status.HTTP_404_NOT_FOUND)

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TestAuthenticatedUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data= {
            'msg': 'Working'
        }
        return Response(data, status=status.HTTP_200_OK)

class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    
    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception = True)
        return Response({'message': "a link has been provided to reset password",}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(GenericAPIView):
       
    def get(self, request, uidb64, token):

        try:
            # user_id = setattr(urlsafe_base64_decode(uidb64))
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': "Token is invalid or expired",}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': " credentials is valid", 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'message': "Token is invalid or expired",}, status=status.HTTP_401_UNAUTHORIZED)
        
class SetNewPasswordView(GenericAPIView):

    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)
        return Response({'message': "Password reset successful",}, status=status.HTTP_200_OK)

class UsersViewsetWithFilterView(viewsets.ModelViewSet):
    queryset = User.objects.filter(
        is_verified=True, 
    )
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    serializer_class = UserSerializer
    ordering_fields = ['id',]
    ordering = ['id']

class AdditionalInfoViewsetWithFilterView(viewsets.ModelViewSet):
    queryset = AdditionalPersonalInfo.objects.all()
    serializer_class = AdditionalInfoSerializer
    ordering_fields = ['id',]
    ordering = ['id']


# class MyProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         serializer = MyProfileSerializer(user)
#         return Response(serializer.data)   


class MyProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Ensure the logged-in user is updating their own profile
        return User.objects.filter(id=self.request.user.id)

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            print(f"Error in partial_update: {e}")  # Debugging output
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def update(self, request, *args, **kwargs):
        """Handle PUT requests for full updates."""
        return super().update(request, *args, **kwargs)

  
 