from django.contrib import admin
from .models import Category, Post, Author, Comment


def null_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


null_rating.short_description = 'Обнулить рейтинг постов'


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author', 'post_time', 'have_rating']
    list_filter = ('author', 'post_time')
    search_fields = ('title', 'categories__name')
    actions = [null_rating]


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
