from django.urls import path
from .views import (AddBooks, GetListedBooks, 
                    GetPersonalRecommendations, RequestForBook,
                    ApproveBookRequest, GetListOfApprovalBooks
                    )

urlpatterns = [
    # path('/aa', admin.site.urls),
    #     path('get-books/', GetListedBooks.as_view()),
    path('get-books/', GetListedBooks.as_view()),
    path('add-books/', AddBooks.as_view()),
    path('get-personal-recommendations/', GetPersonalRecommendations.as_view()),
    path('request-for-book/', RequestForBook.as_view()),
    path('approval-list/', GetListOfApprovalBooks.as_view()),
    path('approve-request/', ApproveBookRequest.as_view())
]
