from django.contrib.auth.admin import UserAdmin


class UserAdminModel(UserAdmin):
    readonly_fields = ['date_joined']
