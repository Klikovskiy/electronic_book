from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.template.loader import render_to_string


def sending_engineer(request, user, message_title, message_tex):
    current_site = get_current_site(request)
    subject = message_title
    message = render_to_string(
        'instructions/email/sending_mailing.html',
        {
            'domain': current_site.domain,
            'message_tex': message_tex,
            'message_title': message_title,
        }
    )
    user.email_user(subject, message, html_message=message)


def paginator(request, posts):
    page_number = request.GET.get('page')
    return Paginator(posts, 10).get_page(page_number)
