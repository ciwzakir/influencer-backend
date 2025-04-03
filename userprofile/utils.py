import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings 


def generateOtp():
    otp = ''
    for i in range(6):
        otp += str(random.randint(0, 9))
    return otp


def send_code_to_user(email):
    subjects = "One time pass code for email verification "
    otp_code = generateOtp()
    print(otp_code)
    user = User.objects.get(email=email)
    current_site = "myauth.com"
    email_body = f"Hi {user.first_name} thanks for signing up {current_site} your otp {otp_code}"
    from_email = settings.DEFAULT_SENDER_EMAIL

    OneTimePassword.objects.create(user=user, code=otp_code)
    despatch_email = EmailMessage(subject=subjects, body=email_body, from_email=from_email, to=[email])
    despatch_email.send(fail_silently=True)

def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']],
    )
    email.send()