from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from news.models import Category, Post


@shared_task
def send_email_to_subscribers_task(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return

    categories = post.categories.all()
    subscribers = User.objects.filter(subscribed_categories__in=categories).distinct()
    for subscriber in subscribers:
        subject = f'Новый пост в категории {post.categories}'
        message = (f'Пост: {post.title}\n\n{post.content[:30]}...\n\nПрочитать полностью: {settings.SITE_URL}'
                   f'{reverse("news_detail", args=[post.pk])}')
        recipient_list = [subscriber.email]

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


@shared_task
def send_email_every_week_task():
    one_week = timezone.now() - timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        posts = Post.objects.filter(post_time__gte=one_week, categories=category)
        if not posts.exists():
            continue

        subscribers = User.objects.filter(subscribed_categories=category)
        if not subscribers.exists():
            continue

        for subscriber in subscribers:
            subject = f"Еженедельная рассылка постов для категории {category.name}"
            message = "Новые посты за неделю:\n\n"
            for post in posts:
                post_url = f"{settings.SITE_URL}/news/{post.pk}"
                message += f"{post.title} - {post_url}\n\n"

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
