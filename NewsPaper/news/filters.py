from django import forms
from django_filters import FilterSet, ChoiceFilter, DateFilter, CharFilter
from .models import Post


class NewsFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        label='Заголовок',
        lookup_expr='icontains',
    )

    author = ChoiceFilter(
        field_name='author__user__username',
        choices=Post.objects.values_list('author__user__username', 'author__user__username').distinct(),
        label='Автор'
    )

    post_time_after = DateFilter(
        field_name='post_time',
        label='Опубликовано после',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
