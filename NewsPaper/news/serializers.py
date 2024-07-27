from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Author
        fields = ['id', 'user', 'rating']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'post_type', 'post_time', 'categories', 'title', 'content', 'rating']


class CategorySerializer(serializers.ModelSerializer):
    subscribers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subscribers']
