from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (LoginSerializer, RegisterSerializer,
                          get_tokens_for_user)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": "Registration failed", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)
            return Response(
                {"user": serializer.data, "token": tokens}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Login Failed", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Logged out"})
            except Exception as e:
                return Response(
                    {"error": "Invalid token", "detail": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Refresh toke is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
