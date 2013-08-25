from django import template

register = template.Library()

@register.filter
def round_float(value):
    return (float(int((value*10)+0.5))/10).__str__()