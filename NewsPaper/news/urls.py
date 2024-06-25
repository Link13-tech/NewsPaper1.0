from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleUpdate, ArticleDelete, \
    subscribe_to_category
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60*1)(NewsList.as_view()), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_create'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_create'),
    path('category/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
]
