from django.contrib.auth.validators import ASCIIUsernameValidator
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
)
from rest_framework.validators import UniqueValidator, ValidationError

from .constants import *
from .models import Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "username",
            "account_name",
            "cin_number",
            "email",
            "password",
            "repeated_password",
        )

    username = CharField(
        min_length=MODEL_CHARFIELD_MIN_LENGTH,
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        trim_whitespace=True,
        allow_blank=False,
        allow_null=False,
        required=True,
        validators=[
            ASCIIUsernameValidator(),
            UniqueValidator(
                queryset=Account.objects.all(),
                message="A company with that username already exists.",
            ),
        ],
    )
    account_name = CharField(
        min_length=MODEL_CHARFIELD_MIN_LENGTH,
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        trim_whitespace=True,
        allow_blank=False,
        allow_null=False,
        required=True,
    )
    cin_number = CharField(
        min_length=CIN_LENGTH,
        max_length=CIN_LENGTH,
        allow_blank=False,
        allow_null=False,
        required=True,
        validators=[
            UniqueValidator(
                queryset=Account.objects.all(),
                message="A company with that CIN already exists.",
            )
        ],
    )
    email = EmailField(
        trim_whitespace=True,
        allow_blank=False,
        allow_null=False,
        required=True,
        validators=[
            UniqueValidator(
                queryset=Account.objects.all(),
                message="A company with that email address already exists.",
            )
        ],
    )
    password = CharField(
        min_length=MODEL_CHARFIELD_MIN_LENGTH,
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True,
    )
    repeated_password = CharField(
        min_length=MODEL_CHARFIELD_MIN_LENGTH,
        max_length=MODEL_CHARFIELD_MAX_LENGTH,
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True,
    )

    # Following two methods need fixing. Validation logics related to two or more fields should be in the validate() method.

    def validate_password(self, value):
        if value != self.initial_data["repeated_password"]:
            raise ValidationError("Passwords do not match.")
        return value

    def validate_repeated_password(self, value):
        if value != self.initial_data["password"]:
            raise ValidationError("Passwords do not match.")
        return value

    def save(self, **kwargs):
        self.validated_data.pop("repeated_password")
        return super().save(**kwargs)


class ActivationSerializer(Serializer):
    email = EmailField(
        trim_whitespace=True,
        allow_blank=False,
        allow_null=False,
        required=True,
    )

    def validate_email(self, value):
        if not Account.objects.filter(email=value).exists():
            raise ValidationError("Invalid email. No user with the given email found.")

        return value
