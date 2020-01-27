from django import template

#https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/


register = template.Library()

@register.filter
def my_index(values, i): #, *args, **kwargs):
    """return element of list by index

    Arguments:
        values {list} -- list
        i {int} - index

    Returns:
        int -- list value by index
    """
    return values[i]

@register.filter
def change_class(class_value, addition):
    """Change class

    Arguments:
        class_value {string} -- class to which should be added addition
        addition {int/str} -- what should be added to class_value

    Returns:
        string -- new class value
    """
    return class_value + str(addition)
