from django import template

register = template.Library()

@register.filter
def addClass(value,arg):
    return value.as_widget(attrs={'class':arg})
