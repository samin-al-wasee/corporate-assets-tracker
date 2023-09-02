from django.urls import path

from .views import (
    AccountActivateView,
    AccountCreateView,
    ReActivateView,
)

app_name = "authentication"

urlpatterns = [
    path(
        "signup/",
        AccountCreateView.as_view(),
        name="signup",
    ),
    path(
        "activate/<str:activation_token>",
        AccountActivateView.as_view(),
        name="activation",
    ),
    path(
        "re-activation/",
        ReActivateView.as_view(),
        name="resend-activation",
    ),
]
