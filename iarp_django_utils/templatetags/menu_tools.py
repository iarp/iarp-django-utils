from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def menu_item_active(context, value, display_hide=False):
    try:
        view_name = context["request"].resolver_match.view_name
    except:  # noqa
        return ""

    default = "" if not display_hide else "display-hide"

    if isinstance(value, list):
        return "active open" if view_name in value else default
    else:
        return "active open" if view_name == value else default
