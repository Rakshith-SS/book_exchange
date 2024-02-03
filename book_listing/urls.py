from django.urls import path
from .views import AddBooks, GetListedBooks, GetPersonalRecommendations

urlpatterns = [
    # path('/aa', admin.site.urls),
    #     path('get-books/', GetListedBooks.as_view()),
    path('get-books/', GetListedBooks.as_view()),
    path('add-books/', AddBooks.as_view()),
    path('get-personal-recommendations/', GetPersonalRecommendations.as_view())
]
