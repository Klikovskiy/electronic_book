from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.forms.widgets import PasswordInput
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Электронная почта',
        'type': 'email'
    }))


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'form-control form-control-lg',
                                          'placeholder': 'Пароль', }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'form-control form-control-lg',
                                          'placeholder': 'Повтор пароля',
                                          }),
    )


class LoginUserForm(AuthenticationForm):
    """
    Форма входа пользователя.
    """

    redirect_authenticated_user = True

    password = forms.CharField(
        label='Пароль',
        widget=PasswordInput(attrs={'class': 'form-control form-control-lg',
                                    'placeholder': 'Пароль',
                                    'type': 'password'})
    )

    username = forms.CharField(
        label='Электронная почта',
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg',
                   'placeholder': 'Электронная почта',
                   'type': 'email'}
        )
    )

    field_order = ['username', 'password']
