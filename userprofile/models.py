from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    # Override groups and user_permissions to avoid reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.email
    
    @property
    def get_full_names(self):
        return f"{self.first_name} {self.last_name}"
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        access_token = refresh.access_token
        
        try:
            membership_info = self.membershipinfo
            access_token['user_role'] = membership_info.user_role
        except MembershipInfo.DoesNotExist:
            access_token['user_role'] = None

        return {
            'refresh': str(refresh),
            'access': str(access_token),
        }


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)


class MembershipInfo(models.Model):
    SUPER_USER = 'superuser'
    ADMIN = 'admin'
    OTHER = 'others'

    USER_STATUS_CHOICES = [
        (SUPER_USER, 'Super User'),
        (ADMIN, 'Admin'),
        (OTHER, 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_bio = models.TextField(verbose_name="Short Bio", help_text="Maximum 230-80 words")

    def clean(self):
        word_count = len(self.short_bio.split())
        if word_count > 150:
            raise ValidationError(f'The bio must not exceed 150 words. It currently has {word_count} words.')
        elif word_count < 50:
            raise ValidationError(f'The bio must be at least 50 words. It currently has {word_count} words.')
        
    share = models.DecimalField(
        null=True,
        max_digits=5,
        decimal_places=2
    )
    user_role = models.CharField(
        max_length=10,
        choices=USER_STATUS_CHOICES,
        default=OTHER,
    )

    def __str__(self):
        return self.user.first_name


class AdditionalPersonalInfo(models.Model):
    MALE = 'male'
    FEMALE = 'female'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    
    MARRIED = 'married'
    UNMARRIED = 'unmarried'

    MARITAL_STATUS_CHOICES = [
        (MARRIED, 'Married'),
        (UNMARRIED, 'Unmarried'),
    ]

    A_POSITIVE = 'A+'
    A_NEGATIVE = 'A-'
    B_POSITIVE = 'B+'
    B_NEGATIVE = 'B-'
    AB_POSITIVE = 'AB+'
    AB_NEGATIVE = 'AB-'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'

    BLOOD_GROUP_CHOICES = [
        (A_POSITIVE, 'A+'),
        (A_NEGATIVE, 'A-'),
        (B_POSITIVE, 'B+'),
        (B_NEGATIVE, 'B-'),
        (AB_POSITIVE, 'AB+'),
        (AB_NEGATIVE, 'AB-'),
        (O_POSITIVE, 'O+'),
        (O_NEGATIVE, 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=255, verbose_name="Father's Name", null=True)
    mother_name = models.CharField(max_length=255, verbose_name="Mother's Name", null=True)
    profile_picture = models.ImageField(
        verbose_name="Profile Picture",
        blank=True,
        upload_to='images/profile'
    )
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default=None,
        blank=True,
        null=True,
    )
    marital_status = models.CharField(
        max_length=9,
        choices=MARITAL_STATUS_CHOICES,
        default=None,
        blank=True,
        null=True,
    )
    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        default=None,
        blank=True,
        null=True,
    )
    dob = models.DateField(verbose_name="Date of Birth")
    nationality = models.CharField(max_length=20)
    present_address = models.CharField(max_length=255)
    permanent_address = models.CharField(max_length=255)
    employment_address = models.CharField(max_length=255, help_text="e.g., Bangladesh Army")
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d+$', 'Phone number must contain only digits.')],
    )

    def __str__(self):
        return self.user.first_name


class Qualification(models.Model):
    user = models.ForeignKey(User, related_name='qualifications', on_delete=models.CASCADE)
    certification = models.CharField(max_length=100, help_text="Like LLB")
    institute_name = models.CharField(max_length=150)
    graduation_year = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Qualification"
        verbose_name_plural = "Qualifications"

    def __str__(self):
        return f"{self.certification} from {self.institute_name}"
    

class WorkExperience(models.Model):
    user = models.ForeignKey(User, related_name='work', on_delete=models.CASCADE)
    experiences = models.TextField(verbose_name="Your Experience", help_text="Maximum 100 words")

    def clean(self):
        word_count = len(self.experiences.split())
        if word_count > 70:
            raise ValidationError(f'The experience must not exceed 70 words. It currently has {word_count} words.')

    def __str__(self):
        return self.user.first_name