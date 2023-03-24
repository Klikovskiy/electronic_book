# Generated by Django 4.1.5 on 2023-03-24 17:22

import ckeditor_uploader.fields
from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titles', models.CharField(max_length=120, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('full_content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текст новости')),
                ('news_picture', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=75, scale=None, size=[830, 430], upload_to='news_img/%Y/%m/', verbose_name='Картинка на главной')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('published', models.BooleanField(default=False, verbose_name='Отображать на сайте')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['date_created'],
            },
        ),
    ]
