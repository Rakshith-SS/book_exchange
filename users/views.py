from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .serializers import (
    RegisterUserSerializer,
)
from rest_framework.permissions import IsAuthenticated

from .models import User, InterestedTopic, BooksRequested
from book_listing.models import ListedBooks
from book_listing.helpers import get_user_id_dict


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
    # permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        user_id = user.id
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
            # Check if the book is available in
            # Table
            book_id = listed_book.id
            book_lended = BooksRequested.objects.filter(
                issuer_user_id=user_id, book_id=book_id).first()
            if book_lended is not None:
                book_state = book_lended.book_state
                if book_state == 1:
                    book_status = "Book Under request approval."
                # borrower_user_id = book_lended.borrower_user_id
                if book_state == 2:
                    book_status = "Book has been exchanged."
            else:
                book_status = "Request For Access."
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
            data["book_status"] = book_status
            data["added_by_users_list"] = get_user_id_dict(
                listed_book.added_by_user_ids)
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
            "wallet_balance": user_wallet_detail,
            "user_id": user.id,
            "username": user.username
        }
        return Response(resp, status=status.HTTP_200_OK)
