from django.http import Http404
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Account, Token
from .permissions import IsNotAuthenticated
from .serializers import AccountSerializer, ActivationSerializer


# Create your views here.
class AccountCreateView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsNotAuthenticated]

    def get_view_name(self):
        return "Register Your Company"

    def perform_create(self, serializer: AccountSerializer) -> None:
        current_user: Account = serializer.save()
        current_user.send_activation_email(being_resent=False)

    def permission_denied(self, request: Request, message=None, code=None) -> None:
        if request.user.is_staff:
            raise PermissionDenied(
                "Please visit the admin panel to register on behalf of new companies."
            )
        if request.user.is_authenticated:
            raise PermissionDenied(
                "You have already signed up and are currently logged in."
            )
        super().permission_denied(request, message, code)


class AccountActivateView(RetrieveAPIView):
    queryset = Token.objects.all()
    permission_classes = [IsNotAuthenticated]
    lookup_field = "activation_token"
    lookup_url_kwarg = "activation_token"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_view_name(self):
        return "Account Activation."

    def retrieve(self, request, *args, **kwargs):
        try:
            token_instance: Token = self.get_object()
            if timezone.now() > token_instance.expires_at:
                raise AuthenticationFailed(
                    "This link is expired. Please request for a new link."
                )
            target_account_instance: Account = token_instance.target_user
            if target_account_instance.is_active:
                return Response(
                    {"message": "Account already activated. Please log in to continue."}
                )
            target_account_instance.is_active = True
            target_account_instance.save()
            return Response({"message": "Account successfully activated."})
        except Http404:
            raise NotFound("Invalid activation token.")

    def permission_denied(self, request: Request, message=None, code=None) -> None:
        if request.user.is_staff:
            raise PermissionDenied(
                "Please visit the admin panel to activate accounts manually."
            )
        if request.user.is_authenticated:
            raise PermissionDenied(
                "Your account is already activated and you are currently logged in."
            )
        super().permission_denied(request, message, code)


class ReActivateView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = ActivationSerializer
    permission_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        response: Response = super().create(request, *args, **kwargs)
        response.data = {"message": "Activation email resent successfully."}
        return response

    def perform_create(self, serializer: ActivationSerializer):
        target_user: Account = self.queryset.get(
            email=serializer.validated_data["email"]
        )
        target_user.send_activation_email(being_resent=True)

    def permission_denied(self, request: Request, message=None, code=None) -> None:
        if request.user.is_staff:
            raise PermissionDenied(
                "Please visit the admin panel to activate accounts manually."
            )
        if request.user.is_authenticated:
            raise PermissionDenied(
                "Your account is already activated and you are currently logged in."
            )
        super().permission_denied(request, message, code)
