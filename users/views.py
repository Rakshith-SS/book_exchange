from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .serializers import (
    RegisterUserSerializer,
)
from rest_framework.permissions import IsAuthenticated

from .models import User, InterestedTopic
from book_listing.models import ListedBooks


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
                    refresh.access_token)}
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


class UserProfileAPI(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response({
                "message": "success",
                "data": {
                    "username": "",
                    "short_description": "",
                    "books_uploaded_by_user": []
                }
            }, status=status.HTTP_200_OK)

        data_resp = {}
        data_resp["username"] = user.username
        data_resp["short_description"] = user.short_description

        listed_books = ListedBooks.objects.filter(is_deleted=False).all()
        output_resp = []
        for listed_book in listed_books:
            data = {}
            data['created_at'] = listed_book.created_at.strftime(
                "%Y-%m-%d %H:%M:%S")
            data['updated_at'] = listed_book.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S")
            data["created_at"] = listed_book.created_at
            data["updated_at"] = listed_book.updated_at
            data["book_name"] = listed_book.book_name
            data["added_by_user_ids"] = listed_book.added_by_user_ids
            data["description"] = listed_book.description
            data["added_by_users"] = listed_book.added_by_users
            data["rating"] = listed_book.rating
            # data["rating"] = listed_book.rating
            data["id"] = listed_book.id
            output_resp.append(data)

        data_resp["books_uploaded_by_user"] = output_resp

        return Response({
            "message": "success",
            "data": data_resp
        }, status=status.HTTP_200_OK)


class GetUserWalletAccountInfo(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_id = request.user.id

        user = User.objects.filter(id=user_id).first()

        if user is None:
            return Response({
                "message": "User Doesn't Exist/Token Expired"
            }, status=status.HTTP_200_OK)

        user_wallet_detail = user.wallet
        resp = {
            "message": "success",
            "wallet_balance": user_wallet_detail
        }
        return Response(resp, status=status.HTTP_200_OK)
