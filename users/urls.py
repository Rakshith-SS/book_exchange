from django.urls import path
from .views import RegisterUserViews, InterestedTopicView, LoginUser

urlpatterns = [
    # path('/aa', admin.site.urls),
    path('register-user/', RegisterUserViews.as_view()),
    path('interested-topics/', InterestedTopicView.as_view()),
    path('login-user/', LoginUser.as_view()),
]
