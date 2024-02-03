from django.urls import path
from .views import AddBooks, GetListedBooks

urlpatterns = [
    # path('/aa', admin.site.urls),
#     path('get-books/', GetListedBooks.as_view()),
    path('get-books/', GetListedBooks.as_view()),
    path('add-books/', AddBooks.as_view())
]
