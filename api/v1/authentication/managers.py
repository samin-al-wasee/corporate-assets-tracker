from typing import Any

from django.contrib.auth.models import UserManager


class AccountManager(UserManager):
    def create_user(
        self,
        username: str,
        email: str | None = ...,
        password: str | None = ...,
        **extra_fields: Any
    ) -> Any:
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        username: str,
        email: str | None = ...,
        password: str | None = ...,
        **extra_fields: Any
    ) -> Any:
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        return super().create_superuser(username, email, password, **extra_fields)

    def create(self, **kwargs: Any) -> Any:
        kwargs_ = kwargs.copy()
        username = kwargs_.pop("username")
        email = kwargs_.pop("email")
        password = kwargs_.pop("password")
        return self.create_user(
            username=username, email=email, password=password, **kwargs_
        )
