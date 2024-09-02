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
    path("<str:username>/", views.profil, name="profil"),
]
