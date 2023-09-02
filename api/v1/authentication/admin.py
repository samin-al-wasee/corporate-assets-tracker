from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Account, Token


class AccountAdmin(UserAdmin):
    fieldsets = (
        (_("Credentials"), {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "account_name",
                    "cin_number",
                    "email",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    list_display = (
        "account_name",
        "username",
        "email",
        "is_active",
        "is_superuser",
        "date_joined",
    )


class TokenAdmin(admin.ModelAdmin):
    list_display = ("activation_token", "target_user", "created_at", "expires_at")


# Register your models here.
admin.site.register(model_or_iterable=Account, admin_class=AccountAdmin)
admin.site.register(model_or_iterable=Token, admin_class=TokenAdmin)
