import django_filters
from rest_framework import viewsets
from rest_framework import permissions

from news.serializers import *
from news.models import *


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешены безопасные методы (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешены изменения только автору
        return obj.author == request.user or request.user.is_staff


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['user', 'rating']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NewsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='NE')
    serializer_class = PostSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['title', 'categories']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='AR')
    serializer_class = PostSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['title', 'categories']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'subscribers']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
