from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post
from .filters import NewsFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.all()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'post'


class NewsSearch(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'flatpages/news_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filterset = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NE'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != 'NE':
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news_list')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != 'NE':
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != 'AR':
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news_list')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != 'AR':
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
