from django import template

register = template.Library()

@register.filter
def round_float(value):
    return int(float(value+0.5)).__str__()