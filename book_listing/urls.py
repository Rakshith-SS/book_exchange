from django.urls import path
from .views import AddBooks, GetListedBooks, GetListedBooks2

urlpatterns = [
    # path('/aa', admin.site.urls),
    path('add-books/', AddBooks.as_view()),
#     path('get-books/', GetListedBooks.as_view()),
    path('get-books/', GetListedBooks2.as_view())
]
