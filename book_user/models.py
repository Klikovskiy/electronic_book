from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from book_instructions.models import Positions, Subdivision


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('E-Mail is Required, Please Provide Your E-Mail.')
        if not first_name:
            raise ValueError(
                'E-Mail is Required, Please Provide Your First Name.')
        if not last_name:
            raise ValueError(
                'E-Mail is Required, Please Provide Your Last Name.')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class BookUser(AbstractUser):
    objects = UserManager()

    username = models.CharField(
        default='-не используется-',
        max_length=150,
        verbose_name='Имя пользователя',
        unique=False,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        max_length=254,
        null=False,
        blank=False,
        unique=True
    )

    position = models.ForeignKey(Positions,
                                 on_delete=models.CASCADE,
                                 verbose_name='Должность',
                                 null=True)

    subdivision = models.ForeignKey(Subdivision,
                                    on_delete=models.CASCADE,
                                    verbose_name='Подразделение',
                                    null=True,
                                    related_name='user_subdivision')

    chief_status = models.BooleanField(default=False,
                                       verbose_name='Статус главы',
                                       help_text='Пользователь получит '
                                                 'доступ к всем службам '
                                                 'и предписаниям.',
                                       null=True, )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
