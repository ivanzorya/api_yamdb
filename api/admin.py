from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm
from .models import User, Comment, Review, Title, Category, Genre, Rate


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'is_admin', 'role', 'username')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    list_editable = ('role', 'username')


class RoleAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    list_filter = ("title",)
    empty_value_display = "-пусто-"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "text", "author", "score", "pub_date")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "review", "text", "author", "pub_date")


class RateAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "sum_vote", "count_vote")


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "rating", "description", "category")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
