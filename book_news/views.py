from django.views.generic import DetailView, ListView

from book_news.models import BookContent


class GetAllNews(ListView):
    """
    Новости на главной.
    """
    model = BookContent
    template_name = 'instructions/home_news.html'
    context_object_name = 'all_news'
    paginate_by = 4


class GetOneNews(DetailView):
    """
    Просмотр отдельной новости.
    """
    model = BookContent
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    template_name = 'instructions/single_news.html'
    context_object_name = 'single_news'
    allow_empty = False
