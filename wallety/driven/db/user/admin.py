from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from driven.db.user.models import UserDBO


admin.site.register(UserDBO, UserAdmin)
