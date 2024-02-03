from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import (
    JWTStatelessUserAuthentication
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .serializers import (
    RegisterUserSerializer,
    LoginUserSerializer,
)
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken
)
from .models import User
import random


class RegisterUserViews(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(
                serializer.validated_data["password"])
            serializer.save()
            return Response(
                {
                    "message": "Successfully registered user"
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "message": "Registration Failed",
                    "data": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


"""
class LoginUser(APIView):
    #    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data["username"],
                                password=serializer.data["password"]
                                )
            if user is not None:
                refresh = RefreshToken.for_user(user)
                data = {"access_token": str(
                    refresh.access_token), "refresh_token": str(refresh)}
                message = f"sent otp to {user.email} mail successfully"
                random_number = random.randint(100000, 999999)

                send_otp(user.email, random_number)

                if user.login_otp is not None:
                    user.login_otp = ""
                user.login_otp = random_number
                user.save()
                return Response(
                    {
                        "message": message,
                        "data": data
                    },

                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": "Invalid username or password"
                    },
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {
                    "message": "Incorrect username or password were provided",
                    "data": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

            """
