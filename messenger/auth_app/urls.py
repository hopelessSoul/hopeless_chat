from django.urls import path
from .views import SignUpView, SingInView, SignOutView, LoggedInUser

app_name = "auth_app"

urlpatterns = [
    path('sign-up', SignUpView.as_view(), name='sign_up'),
    path('sign-in', SingInView.as_view(), name='sign_in'),
    path('logout', SignOutView.as_view(), name='logout'),
    path('', LoggedInUser.as_view(), name='current_user'),
]
