from django import template


register = template.Library()


@register.filter(name="user_in_group")
def user_in_group(user, group_names):
    """Returns boolean if the supplied user is in any
    one of the groups supplied in a comma separated list.

    Examples:

         {{ user|user_in_group:"Human Resources,Warehouse" }}

    """
    return user.groups.filter(name__in=group_names.split(",")).exists()
