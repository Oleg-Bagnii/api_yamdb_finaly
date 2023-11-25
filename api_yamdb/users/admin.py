from django.contrib import admin

from reviews.models import Genre, Category
from .models import User

admin.site.register(Genre)
admin.site.register(Category)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("username", "email", "first_name", "last_name", "bio", "role")
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "bio",
        "role",
    )
    list_editable = ("role",)
