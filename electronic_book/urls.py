from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from book_user.forms import UserPasswordResetForm, UserSetPasswordForm

urlpatterns = [
    path('', include('book_instructions.urls', namespace='book_instructions')),
    path('news/', include('book_news.urls', namespace='book_news')),
    path('admin/', admin.site.urls),
    path('user/', include('book_user.urls', namespace='book_user')),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='user/password/password_reset.html',
        form_class=UserPasswordResetForm),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='user/password/password_sent.html'),
         name='password_reset_done', ),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password/password_confirm.html',
             form_class=UserSetPasswordForm),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password/password_complete.html'),
         name='password_reset_complete'),
    path('change-password/',
         auth_views.PasswordChangeView.as_view(
             template_name='user/password/change-password.html',
             success_url='/'), name='change_password'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
