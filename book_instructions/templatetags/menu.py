from django import template

from book_instructions.models import Services

register = template.Library()


@register.inclusion_tag('instructions/include/general_items_menu.html')
@register.simple_tag(takes_context=True)
def general_menu(request):
    services_menu = Services.objects.all()
    return {'services_menu': services_menu, 'request': request}
