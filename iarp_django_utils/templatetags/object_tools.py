from django.template.defaulttags import register


@register.filter
def get_object_attribute(o, attr, default=''):
    """ This is a shortcut filter that reduces if statements
    when wanting a default value.

    Examples:

        {{ previous_evaluation|get_object_attribute:"Assists|0" }}

        is the same as:

        {% if previous_evaluation.Assists %}
            {{ previous_evaluation.Assists }}
        {% else %}
            0
        {% endif %}

    """

    try:
        attr, default = attr.split('|', 1)
    except ValueError:
        pass

    if default.isdigit():
        default = int(default)

    return getattr(o, attr, default)
