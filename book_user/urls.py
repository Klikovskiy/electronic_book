from django.contrib.auth import views as auth_views
from django.urls import path

from book_user.views import LoginUser, GetUserProfile

app_name = 'book_user'

urlpatterns = [
    path('login/', LoginUser.as_view(redirect_authenticated_user=True),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='user/logout.html'),
         name='logout'),
    path('profile/<int:pk>/', GetUserProfile.as_view(),
         name='user_profile'),
]
