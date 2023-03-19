from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse_lazy
from django_resized import ResizedImageField


class BookContent(models.Model):
    """
    Новостной блок.
    """
    titles = models.CharField(max_length=120, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='URL',
                            unique=True)
    full_content = RichTextUploadingField('Текст новости')
    news_picture = ResizedImageField(size=[830, 430],
                                     crop=['middle', 'center'],
                                     force_format='JPEG',
                                     quality=75,
                                     upload_to='news_img/%Y/%m/',
                                     blank=True,
                                     null=True,
                                     verbose_name='Картинка на главной', )
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Дата создания')
    published = models.BooleanField(default=False,
                                    verbose_name='Отображать на сайте')

    def __str__(self):
        return self.titles

    def get_absolute_url(self):
        return reverse_lazy('content', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['date_created']
