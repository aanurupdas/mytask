from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken


def generate_email(user, to_email, subject=" "):
    current_site = settings.CURRENT_SITE
    token = RefreshToken.for_user(user).access_token
    activation_link = f"{current_site}/verify-user/{token}/"
    message = "Hello {0},\n{1}".format(user.first_name, activation_link)
    email = EmailMessage(subject, message, "admin@example.in", to=[to_email])

    email.send()

    return email


def user_tokens(user):
    refresh = RefreshToken.for_user(user)
    accessToken = refresh.access_token
    return {
        "access": str(accessToken),
        "refresh": str(refresh),
    }
