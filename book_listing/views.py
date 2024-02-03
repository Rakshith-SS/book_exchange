from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ListedBooks
from .serializer import AddBookSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import User


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
                ]
            }, status=status.HTTP_200_OK)


class AddBooks(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data
            user_id = request.user.id
            book_name = data.get("book_name", None)
            author_name = data.get("author_name", None)
            description = data.get("description", None)
            rating = data.get("rating", None)
            topics = data.get("topics", None)

            user = User.objects.filter(id=user_id).first()
            if topics is None:
                return Response({
                    "message": "Topics are not Selected"
                }, status=status.HTTP_400_BAD_REQUEST)

            if user is not None:
                username = user.username

            if book_name is None:
                return Response({
                    "message": "Book Name is required"
                }, status=status.HTTP_400_BAD_REQUEST)
            listed_book = ListedBooks.objects.filter(
                book_name=book_name).first()
            if listed_book is not None:
                added_by_user_ids = listed_book.added_by_user_ids
                added_by_users = listed_book.added_by_users

                if user_id not in added_by_user_ids:
                    added_by_user_ids.append(user_id)

                if username not in added_by_users:
                    added_by_users.append(username)

                ListedBooks.objects.filter(book_name=book_name).update(
                    added_by_user_ids=added_by_user_ids,
                    added_by_users=added_by_users
                )
                return Response(
                    {
                        "message": "success"
                    })
            else:
                # pass
                listed_book = ListedBooks(
                    added_by_user_ids=[user_id],
                    book_name=book_name,
                    author_name=author_name,
                    description=description,
                    added_by_users=[username],
                    rating=rating,
                    topics=topics
                )
                listed_book.save()

                return Response({
                    "message": "success"
                })
        except Exception as e:
            print(e)
            return Response({
                "message": "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)


class GetPersonalRecommendations(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_id = request.user.id

        user = User.objects.filter(id=user_id).first()
        if user is not None:
            interested_topics = user.interests
            output_resp = []
            check_book = []
            for interested_topic in interested_topics:
                listed_books = ListedBooks.objects.filter(
                    topics__contains=[interested_topic]
                )
                for listed_book in listed_books:
                    if listed_book not in check_book:
                        check_book.append(listed_book)
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

            return Response({
                "message": "success",
                "data": output_resp
            }, status=status.HTTP_200_OK)
