from django.contrib import admin
from .models import Category, Post, Author, Comment, Vote
from modeltranslation.admin import TranslationAdmin


def null_rating(modeladmin, request, queryset):
    for post in queryset:
        post.rating = 0
        post.save()
        Vote.objects.filter(post=post).delete()


null_rating.short_description = 'Обнулить рейтинг постов и удалить все голоса'


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['title', 'content', 'author', 'post_time', 'have_rating']
    list_filter = ('author', 'post_time')
    search_fields = ('title', 'categories__name')
    actions = [null_rating]


class CategoryAdmin(TranslationAdmin):
    model = Category


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
