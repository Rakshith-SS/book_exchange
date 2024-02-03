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
)
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken
)
from .models import User, InterestedTopic


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


class InterestedTopicView(APIView):
    def get(self, request):
        topics = InterestedTopic.objects.first()
        return Response({
            "message": "success",
            "topic_names": topics.interest_names
        })


class LoginUser(APIView):
    #    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        print(data)
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None or password is None:
            return Response({"message": "error", "status": "400", "error_message": "email/password is required"})

        if email is not None and password is not None:
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({"message": "error", "status": "400", "error_messsage": "User doesn't exist."})

            password_check = user.check_password(password)
            if password_check is True:
                refresh = RefreshToken.for_user(user)
                data = {"access_token": str(
                    refresh.access_token) }
                message = "Login Successful"

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
                    status=status.HTTP_400_BAD_REQUEST
                )
