from re import T
from django import template
from django.template.defaultfilters import stringfilter
from ..models import Category
import markdown as md

register = template.Library()

@register.inclusion_tag('mainapp/includes/navigation.html', takes_context=True)
def show_navbar(context):
    context['menu_categories'] = Category.objects.all()
    return context

@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])