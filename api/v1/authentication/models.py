import uuid
from typing import Any

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .constants import *
from .managers import AccountManager


# Create your models here.
class Account(AbstractUser):
    username_validator = None
    username = models.CharField(
        _("username"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False,
        help_text=_(
            "Required. 128 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[
            ASCIIUsernameValidator(),
            MinLengthValidator(MODEL_CHARFIELD_MIN_LENGTH),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = None
    last_name = None
    account_name = models.CharField(
        _("company name"),
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[MinLengthValidator(MODEL_CHARFIELD_MIN_LENGTH)],
    )
    cin_number = models.CharField(
        _("company identification number"),
        max_length=CIN_LENGTH,
        unique=True,
        blank=False,
        null=False,
        validators=[MinLengthValidator(CIN_LENGTH)],
    )
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    objects = AccountManager()
    REQUIRED_FIELDS = ["account_name", "cin_number", "email"]

    def get_full_name(self) -> str:
        return self.account_name.strip()

    def get_short_name(self) -> str:
        pass

    def send_activation_email(self, being_resent: bool) -> None:
        activation_token = uuid.uuid4()
        activation_email = f"Welcome, {self.get_full_name()}. Please visit the following link to activate your account: \nhttp://127.0.0.1:8000/api/v1/accounts/activate/{str(activation_token)}"

        if being_resent:
            Token.objects.filter(target_user=self.id).update(
                activation_token=activation_token,
                created_at=timezone.now(),
                expires_at=timezone.now() + timezone.timedelta(minutes=5.0),
            )
        else:
            Token.objects.create(activation_token=activation_token, target_user=self)

        self.email_user(
            subject="Account Activation/Confirmation.",
            message=activation_email,
            from_email="admin@coastr.cat",
        )


class Token(models.Model):
    activation_token = models.UUIDField(editable=False)
    target_user = models.OneToOneField(
        to=Account, on_delete=models.CASCADE, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    expires_at = models.DateTimeField(editable=False)

    class Meta:
        pass

    def __str__(self) -> str:
        return str(self.activation_token)

    def save(self, *args, **kwargs) -> Any:
        self.created_at = timezone.now() if self.created_at is None else self.created_at
        self.expires_at = (
            timezone.now() + timezone.timedelta(minutes=5.0)
            if self.created_at is None
            else self.created_at + timezone.timedelta(minutes=5.0)
        )
        return super().save(*args, **kwargs)
