from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import BookUser


class BookUserAdmin(UserAdmin):
    model = BookUser

    fieldsets = (
        (None, {'fields': ('position', 'subdivision', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'chief_status',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    # 'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'position',
                    'subdivision')


admin.site.register(BookUser, BookUserAdmin)
