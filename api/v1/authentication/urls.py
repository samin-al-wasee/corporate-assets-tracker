from django.urls import path

from .views import AccountActivateView, AccountCreateView, ReActivateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = "authentication"

urlpatterns = [
    path(
        "signup/",
        AccountCreateView.as_view(),
        name="signup",
    ),
    path(
        "activate/<str:activation_token>/",
        AccountActivateView.as_view(),
        name="activation",
    ),
    path(
        "re-activation/",
        ReActivateView.as_view(),
        name="resend-activation",
    ),
    path(
        "access-token/",
        TokenObtainPairView.as_view(),
        name="access-token",
    ),
    path(
        "refresh-token/",
        TokenRefreshView.as_view(),
        name="refresh-token",
    ),
    path(
        "verify-token/",
        TokenVerifyView.as_view(),
        name="verify-token",
    ),
]
