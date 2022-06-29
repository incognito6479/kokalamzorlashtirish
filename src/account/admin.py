from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from account.models import Organization, User

admin.site.register(Permission)


class UserAdmin(BaseUserAdmin):
    list_display = (
        "phone_number",
        "email",
        "organization",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_filter = (
        "is_active",
        "is_staff",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password",
                )
            },
        ),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "organization")},
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
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "organization",
                )
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User, UserAdmin)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["id", "name", "region", "status"]
