from django import template
from django.contrib.auth.models import User


#https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/


register = template.Library()

@register.filter
def handle_errors(errors):
    error = errors['__all__'][0]
    if 'inactive' in error:
        return "Your account is inactive. Please check your email"
    else:
        return "Your username and password don't match. Please try again."