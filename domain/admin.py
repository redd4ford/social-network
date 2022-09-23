from django.contrib import admin
from domain.models import (
    Like,
    User,
    UserAdminModel,
    Post,
)


admin.site.register(User, UserAdminModel)
admin.site.register(Post)
admin.site.register(Like)
