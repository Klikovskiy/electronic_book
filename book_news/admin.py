from django.contrib import admin

from book_news.models import BookContent


class BookContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('titles',)}
    list_display = (
        'pk',
        'titles',
        'date_created',
        'published')

    list_display_links = ('pk', 'titles',)
    search_fields = ('titles', 'full_content',)


admin.site.register(BookContent, BookContentAdmin)
