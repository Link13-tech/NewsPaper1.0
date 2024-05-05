from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'post'
