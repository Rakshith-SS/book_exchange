from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ListedBooks
from .serializer import AddBookSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import User, BooksRequested
from uuid import uuid4
from .helpers import get_user_id_dict


class GetListedBooks(APIView):
    def get(self, request):
        try:
            listed_books = ListedBooks.objects.filter(is_deleted=False).all()
            output_resp = []
            for listed_book in listed_books:
                # Check if the book is available in
                # Table
                book_id = listed_book.id
                book_lended = BooksRequested.objects.filter(
                    book_id=book_id).first()
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
                added_by_user_ids = listed_book.added_by_user_ids
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
                data["added_by_users_list"] = get_user_id_dict(
                    added_by_user_ids)  # [{"rakshith": 2}, {"sagar": 6}]
                data["added_by_users_list"] = get_user_id_dict(
                    listed_book.added_by_user_ids)
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
                        data["added_by_users_list"] = get_user_id_dict(
                            listed_book.added_by_user_ids)
                        output_resp.append(data)

            return Response({
                "message": "success",
                "data": output_resp
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "success",
            "data": []
        }, status=status.HTTP_200_OK)


class RequestForBook(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user_id = request.user.id
        data = request.data
        issuer_user_id = data["user_id"]
        book_id = data["book_id"]

        if issuer_user_id == user_id:
            return Response({
                "message": "Cannot Self Borrow"
            }, status=status.HTTP_400_BAD_REQUEST)
        # first Search if book id exists in db
        book = ListedBooks.objects.filter(id=book_id,
                                          added_by_user_ids__contains=[
                                              issuer_user_id]).first()

        if book is None:
            return Response({"message": "Book Doesn't Exist.",
                             }, status=status.HTTP_400_BAD_REQUEST)

        if issuer_user_id in book.added_by_user_ids:
            user = User.objects.filter(id=user_id).first()
            if user is not None:
                # Check if book is borrowed previously or Not
                book_check = BooksRequested.objects.filter(
                    book_id=book_id,
                    issuer_user_id=issuer_user_id
                ).first()

                if book_check is not None:
                    if book_check.book_state != 0:
                        return Response({
                            "message": "Book is currently borrowed or requested for approval"
                        }, status=status.HTTP_400_BAD_REQUEST)

                book_request = BooksRequested(
                    book_id=book_id,
                    issuer_user_id=issuer_user_id,
                    borrower_user_id=user_id,
                    book_state=1,
                    request_id=uuid4().hex
                )
                book_request.save()
                return Response({
                    "message": "success",
                }, status=status.HTTP_200_OK)

        return Response({
            "message": "success 4"
        }, status=status.HTTP_200_OK)


class ApproveBookRequest(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        # user_id = request.user.id
        # borrower_user_id = data["borrower_user_id"]
        # book_id = data["book_id"]
        request_id = data["request_id"]

        check_book = BooksRequested.objects.filter(
            request_id=request_id
        ).order_by('-created_at').first()

        if check_book is not None:
            user_id = check_book.borrower_user_id
            user = User.objects.filter(id=user_id).first()
            user.wallet = user.wallet - 10
            user.save()
            BooksRequested.objects.filter(
                request_id=request_id
            ).order_by('-created_at').update(
                book_state=2
            )

        return Response({
            "message": "success"
        }, status=status.HTTP_200_OK)


class GetListOfApprovalBooks(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_id = request.user.id
        books = BooksRequested.objects.filter(
            book_state=1,
            issuer_user_id=user_id
        ).all()

        output_resp = []
        check_book = []
        for book in books:
            listed_books = ListedBooks.objects.filter(
                id=book.book_id
            )
            request_id = book.request_id
            for listed_book in listed_books:
                if listed_book not in check_book:
                    check_book.append(listed_book)
                    data = {}
                    data["request_id"] = request_id
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
