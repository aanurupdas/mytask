from django.http.response import HttpResponse
import jwt

# Django imports
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.conf import settings

# Third Party Imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Local Imports
from users.serializers import (
    UserSignupSerializer,
    PasswordSerializer,
    SigninSerializer,
    UserSerializer,
)
from users.models import User
from users.utils import generate_email, user_tokens

# Create your views here.


def home(request):
    return HttpResponse("Welcome to TODO API")


@api_view(("POST",))
def signup(request):
    # custom serializer to validate user data
    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    email = validated_data.get("email")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = serializer.create(validated_data)

    if user.is_active is True:
        content = {"message": f"{email} already active"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    generate_email(
        user=user,
        to_email=user.email,
        subject="Verification Email - Example",
    )
    content = {"message": f"Activation link send to {email}"}
    return Response(content, status=status.HTTP_201_CREATED)


@api_view(("POST",))
def resend_verification_email(request):
    email = request.POST.get("email")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        content = {"message": f"{email} not exist"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if user.is_active is True:
        content = {"message": f"{email} already active"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    generate_email(
        user,
        to_email=user.email,
        subject="Verification Email - Example",
    )
    content = {"message": f"Activation link send to {email}"}
    return Response(content, status=status.HTTP_200_OK)


@api_view(("PUT",))
def verify_user(request, token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

    except jwt.DecodeError as identifier:
        return Response(
            {"message": "Activation link invalid"}, status=status.HTTP_400_BAD_REQUEST
        )
    except jwt.ExpiredSignatureError as identifier:
        return Response(
            {"message": "Activation link expired"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.get(id=payload["user_id"])
    if user.is_active is True:
        content = {"message": f"{user.email} already active,Sign In"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    serializer = PasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    # create the user with requested password
    user = serializer.create(validated_data, user)
    # activate the user if password has been created
    user.is_active = True
    user.save()

    response = {
        "message": f"{user.email} is now active.",
        "User": UserSerializer(user).data,
        "tokens": user_tokens(user),
    }
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(("POST",))
def signin(request):
    # custom serializer to validate user data
    serializer = SigninSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    email = validated_data.get("email")
    password = validated_data.get("password")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        content = {"message": f"{email} not exist"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if user.is_active is False:
        content = {"message": f"{email} not active, Sign Up"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if user:
        update_last_login(None, user)
        data = {"user": UserSerializer(user).data, "tokens": user_tokens(user)}
        return Response(data)
