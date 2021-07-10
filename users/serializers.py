from rest_framework import serializers
from users.models import User
from django.contrib.auth.password_validation import validate_password


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, min_length=4, required=True)
    first_name = serializers.CharField(max_length=25, required=True)
    last_name = serializers.CharField(max_length=25, required=True)
    is_active = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            is_active=False,
        )
        user.save()

        return user


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=25, validators=[validate_password], required=True
    )
    confirm_password = serializers.CharField(
        max_length=25, validators=[validate_password], required=True
    )

    def validate(self, attrs):

        return super().validate(attrs)

    def create(self, validated_data, user):
        user.set_password(validated_data.get("confirm_password"))
        user.save()

        return user


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, min_length=4, required=True)
    password = serializers.CharField(
        max_length=25, validators=[validate_password], required=True
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
