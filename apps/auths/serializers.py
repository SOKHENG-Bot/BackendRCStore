from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id",)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
    )
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "phone_number",
            "password",
            "confirm_password",
            "avatar_profile",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }

    def validate(self, data):  # Object-level validation (cross-field validation)
        if data["confirm_password"] != data["password"]:
            raise serializers.ValidationError("confirm password must match password")
        return data

    def create(self, validated_data):  # Convert validated data to user model instance
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise serializers.ValidationError("email and password are required")

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError("user not found")
        data["user"] = user
        return data


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        fields = ("access_token", "refresh_token")


# Custom token jwt-simple
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
    }
