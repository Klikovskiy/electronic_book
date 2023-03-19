from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView

from book_user.forms import LoginUserForm
from book_user.models import BookUser


class LoginUser(LoginView):
    """Авторизация пользователя."""

    form_class = LoginUserForm
    template_name = 'user/login.html'
    LOGIN_REDIRECT_URL = 'book_instructions:home'


class GetUserProfile(LoginRequiredMixin, DetailView):
    """Просмотр данных профиля."""

    model = BookUser

    template_name = 'user/profile.html'
    context_object_name = 'user_profile'
    allow_empty = False
