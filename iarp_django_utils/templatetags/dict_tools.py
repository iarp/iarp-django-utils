from django.template.defaulttags import register


@register.filter
def get_dict_value_by_key(dictionary, key):
    """Used when your key is stored in a template variable
        and you need to use it to access a dictionary value

    Examples:

        Where players is a dict like:
            players = {
                123: model instance,
                321, model instance,
            }
        and session_save_status is a dict of player ids that saved during an operation
            session_save_status = {
                123: True,
                321: False,
            }

        {% for player_id, player_data in players.items %}

            {% if session_save_status|get_dict_value_by_key:player_id %}
                Save Successful
            {% else %}
                Save Failed, please try again.
            {% endif %}

        {% endfor %}

    """
    try:
        return dictionary.get(key, dictionary.get(str(key)))
    except (AttributeError, KeyError, TypeError, ValueError):
        return None


@register.filter
def get_subdict_items_by_key(dictionary, key):
    """See get_dict_value_by_key above docstring for explanation,
    in this case it returns .items on the subdict"""
    try:
        return dictionary.get(key, dictionary.get(str(key))).items()
    except (AttributeError, KeyError, TypeError, ValueError):
        return None
