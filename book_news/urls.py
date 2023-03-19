from django.urls import path

from book_news.views import GetAllNews, GetOneNews

app_name = 'book_news'

urlpatterns = [
    path('', GetAllNews.as_view(), name='all_news'),
    path('<str:slug>/', GetOneNews.as_view(), name='single_news'),
]
