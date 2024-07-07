from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = self.user.comment_set.aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comments_rating = self.post_set.aggregate(pcr=Coalesce(Sum('comment__rating'), 0))['pcr']

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    article = 'AR'
    news = 'NE'
    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POSITIONS)
    post_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    @property
    def have_rating(self):
        return self.rating != 0

    def __str__(self):
        return f'{self.title.title()}: {self.content[:20]}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'news-{self.pk}')

    def get_user_vote(self, user):
        return self.vote_set.filter(user=user).first()

    def like(self, user):
        vote, created = Vote.objects.get_or_create(user=user, post=self, defaults={'is_like': True})

        if not created and vote.is_like:
            # Отменяем лайк
            self.rating -= 1
            vote.delete()
        else:
            if not created:
                if not vote.is_like:
                    self.rating += 2  # если был дизлайк, увеличиваем на 2
                else:
                    self.rating += 1
            else:
                self.rating += 1
            vote.is_like = True
            vote.save()
        self.save()

    def dislike(self, user):
        vote, created = Vote.objects.get_or_create(user=user, post=self, defaults={'is_like': True})

        if not created and not vote.is_like:
            # Отменяем дизлайк
            self.rating += 1
            vote.delete()
        else:
            if not created:
                if vote.is_like:
                    self.rating -= 2  # если был лайк, уменьшаем на 2
                else:
                    self.rating -= 1
            else:
                self.rating -= 1
            vote.is_like = False
            vote.save()
        self.save()

    def preview(self):
        return self.content[:124] + '...'

    # def get_absolute_url(self):
    #     return reverse('news_detail', args=[str(self.id)])


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_like = models.BooleanField()

    class Meta:
        unique_together = ('user', 'post')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
