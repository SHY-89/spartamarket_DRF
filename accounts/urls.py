from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views


app_name="accounts"
urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", views.signup, name="signup"),
    path("profil/<str:username>/", views.UserProfilAPIView.as_view(), name="profil"),
    path("password-change/<str:username>/", views.password_change, name="password_change"),
    path("like/<int:user_pk>/", views.like, name="like"),
]
