from django import template

register = template.Library()


@register.filter(name="add", is_safe=True)
def add(number=None, number_op=None):
    return number + number_op


@register.filter(name="sub", is_safe=True)
def sub(number=None, number_op=None):
    return number - number_op
