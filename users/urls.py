from django.urls import path
from .views import RegisterUserViews

urlpatterns = [
    # path('/aa', admin.site.urls),
    path('register-user/', RegisterUserViews.as_view())
]
