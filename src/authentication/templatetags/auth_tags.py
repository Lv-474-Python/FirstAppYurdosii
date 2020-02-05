from django import template

#https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/


register = template.Library()

@register.filter
def handle_errors(errors):
    error = errors['__all__'][0]
    if 'inactive' in error:
        return "Your account is inactive. Please check your email"
    return "Your username and password don't match. Please try again."
