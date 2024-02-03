from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ListedBooks
from .serializer import AddBookSerializer, GetBooksSerializer
from django.core.serializers.json import DjangoJSONEncoder
import json


class GetListedBooks(APIView):
    def get(self, request):
        try:
            # listed_books = ListedBooks.objects.filter(is_deleted=False).all()
            listed_books = ListedBooks.objects.filter(is_deleted=False).all()
            # serialized_q = GetBooksSerializer(data=listed_books, many=True)
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

                # {"sagar": 2}

                output_resp.append(data)
            return Response(
                {"message": "success",
                 "data": output_resp  # serialized_q
                 }, status=200)

        except Exception as e:
            print(e)
            return Response({
                "message": "success",
                "data": [
                    {
                        "added_by_user_ids": [1],
                        "book_name": "Sherlock Holmes",
                        "author_name": "Sir Arthur Conan Doyle",
                        "Description": "A Detective Novel",
                        "Rating": 1,
                        "id": 1
                    }
                ]
            }, status=status.HTTP_200_OK)


class AddBooks(APIView):
    def post(self, request):
        try:
            serializer = AddBookSerializer(data=request.data)
            if serializer.is_valid():
                user_id = serializer.validated_data["user_id"]
                book_name = serializer.validated_data["book_name"]
                author_name = serializer.validated_data["author_name"]
                description = serializer.validated_data["description"]
                added_by_user = serializer.validated_data["added_by_user"]
                rating = serializer.validated_data["rating"]

                listed_book = ListedBooks(
                    added_by_user_ids=[user_id],
                    book_name=book_name,
                    author_name=author_name,
                    description=description,
                    added_by_users=[added_by_user],
                    rating=rating
                )
                listed_book.save()

                return Response({
                    "message": "success"
                })
            else:
                return Response({
                    "message": "error"
                })
        except Exception as e:
            print(e)
            return Response({
                "message": "error"
            })
            pass
