from django import template

register = template.Library()

@register.filter(name='divide',is_safe=True)
def divide(value, arg):
    return value/int(arg)

@register.filter(name='multiply',is_safe=True)
def multiply(value, arg):
    return value*int(arg)
