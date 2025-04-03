from rest_framework import serializers
from .models import User, MembershipInfo, AdditionalPersonalInfo, Qualification, WorkExperience
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.exceptions import AuthenticationFailed
from  django.urls import reverse
from  .utils import send_normal_email
from django.db import transaction



class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2', None)

        if password != password2:
            raise serializers.ValidationError("Passwords don't match.")
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        return user

class MembershipInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipInfo
        fields = "__all__"

class AdditionalPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalPersonalInfo
        fields = "__all__"

class QualificationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = "__all__"

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        # fields = ['id', 'experiences', 'user'] 
        fields = "__all__"
    

class MyProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    member_info = MembershipInfoSerializer(source='membershipinfo', read_only=False)
    personal_info = AdditionalPersonalInfoSerializer(source='additionalpersonalinfo', read_only=False)
    qualifications = QualificationInfoSerializer(many=True, read_only=False)
    experiences_info = WorkExperienceSerializer(source='work', many=True, read_only=False)

    class Meta:
        model = User
        fields = ['id','member_info', 'personal_info', 'qualifications', 'experiences_info', 
                  'email', 'first_name', 'last_name', 'full_name', 
                  'is_staff', 'is_superuser', 'date_joined']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def update(self, instance, validated_data):
        # Update member info
        member_info_data = validated_data.pop('membershipinfo', None)
        if member_info_data:
            MembershipInfo.objects.update_or_create(user=instance, defaults=member_info_data)

        # Update personal info
        personal_info_data = validated_data.pop('additionalpersonalinfo', None)
        if personal_info_data:
            AdditionalPersonalInfo.objects.update_or_create(user=instance, defaults=personal_info_data)

        # Update qualifications
        qualifications_data = validated_data.pop('qualifications', [])
        for qualification in qualifications_data:
            qualification_id = qualification.get('id')
            if qualification_id:
                Qualification.objects.filter(id=qualification_id).update(**qualification)
            else:
                Qualification.objects.create(user=instance, **qualification)

        # Update work experiences
        experiences_info_data = validated_data.pop('work', [])
        for experience in experiences_info_data:
            experience_id = experience.get('id')
            if experience_id:
                WorkExperience.objects.filter(id=experience_id).update(**experience)
            else:
                WorkExperience.objects.create(user=instance, **experience)

        # Update base user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

 

class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalPersonalInfo
        fields = "__all__"  

class UserSerializer(serializers.ModelSerializer):
    member_info = MembershipInfoSerializer(source='membershipinfo', read_only=True)
    personal_info = AdditionalPersonalInfoSerializer(source='additionalpersonalinfo', read_only=True)
    qualifications = QualificationInfoSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id','email','member_info','personal_info','qualifications','first_name','last_name', 'is_staff','is_superuser','is_verified','is_active','date_joined']
        depth = 2

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=70, min_length=10)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token', 'is_staff', 'is_superuser']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        user = authenticate(request, email=email, password=password)
       
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials, try again')

        # Check if the password is correct
        if not user.check_password(password):
            raise AuthenticationFailed('Password does not match, try again')

        # Check if the user is verified
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        

        user_tokens = user.tokens()

        return {
            'email': user.email,
            'full_name': user.get_full_names,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh')),
            'is_staff': user.is_staff, 
            'is_superuser': user.is_superuser, 
        }





class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=70)
    
    class Meta:
        # model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
      
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            abs_link = f"http://{site_domain} {relative_link}"
            email_body = f" Password reset confirmed {abs_link}"

            data= {
                'email_body':email_body,
                'email_subject':f"email subject ...........",
                'to_email':user.email

            }

            send_normal_email(data)
        return super().validate(attrs)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, write_only=True)
    confirm_password = serializers.CharField(max_length=68, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password','confirm_password','uidb64','token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Reset link has expired or invalid')
            if password != confirm_password:
                raise AuthenticationFailed('Password not matched')
            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed('Reset link has expired or invalid')
        return user
 