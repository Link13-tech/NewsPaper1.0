from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import NewsFilter
from .forms import PostForm
from django.core.mail import send_mail
from django.conf import settings
from news.tasks import send_email_to_subscribers_task
import logging

logger = logging.getLogger(__name__)


class NewsList(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_category = self.request.GET.get('category')
        if selected_category:
            queryset = queryset.filter(categories__id=selected_category)
        return queryset.order_by('-post_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_category = self.request.GET.get('category')
        if selected_category:
            filtered_queryset = self.get_queryset().filter(categories__id=selected_category)
        else:
            filtered_queryset = self.get_queryset()
        context['categories'] = Category.objects.all()
        context['selected_category'] = selected_category
        context['total_news'] = filtered_queryset

        if selected_category:
            category = Category.objects.get(id=selected_category)
            context['is_subscribed'] = self.request.user.is_authenticated and category.subscribers.filter(id=self.request.user.id).exists()
        else:
            context['is_subscribed'] = False

        return context


@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    return redirect(reverse('news_list') + f'?category={category_id}')


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


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NE'
        post.save()
        form.save_m2m()
        send_email_to_subscribers_task.delay(post.pk)
        return super().form_valid(form)

    # @staticmethod
    # def send_email_to_subscribers(post):
    #     categories = post.categories.all()
    #     subscribers = User.objects.filter(subscribed_categories__in=categories).distinct()
    #     for subscriber in subscribers:
    #         subject = f'Новая новость в категории'
    #         message = f'Новость: {post.title}\n\n{post.content[:30]}...\n\nПрочитать полностью: {settings.SITE_URL}{reverse("news_detail", args=[post.pk])}'
    #         recipient_list = [subscriber.email]
    #
    #         logger.info(f'Sending email to {subscriber.email}')
    #         logger.info(f'Subject: {subject}')
    #         logger.info(f'Message: {message}')
    #
    #         try:
    #             send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    #             logger.info(f'Email sent to {subscriber.email}')
    #         except Exception as e:
    #             logger.error(f'Error sending email to {subscriber.email}: {e}')


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        post.save()
        form.save_m2m()
        send_email_to_subscribers_task.delay(post.pk)
        return super().form_valid(form)

    # @staticmethod
    # def send_email_to_subscribers(post):
    #     categories = post.categories.all()
    #     subscribers = User.objects.filter(subscribed_categories__in=categories).distinct()
    #     for subscriber in subscribers:
    #         subject = f'Новая статья в категории'
    #         message = f'Статья: {post.title}\n\n{post.content[:30]}...\n\nПрочитать полностью: {settings.SITE_URL}{reverse("news_detail", args=[post.pk])}'
    #         recipient_list = [subscriber.email]
    #
    #         logger.info(f'Sending email to {subscriber.email}')
    #         logger.info(f'Subject: {subject}')
    #         logger.info(f'Message: {message}')
    #
    #         try:
    #             send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    #             logger.info(f'Email sent to {subscriber.email}')
    #         except Exception as e:
    #             logger.error(f'Error sending email to {subscriber.email}: {e}')


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
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


class ArticleUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
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
