from iarp_django_utils.app_settings import app_settings


def only_save_changed_data(obj, obj_data: dict, not_these_fields=None, not_these_fields_startswith=None, save=True):
    """Only save obj where data found in obj_data does not match data within obj.

    Examples:

        >>> obj = MyModel.objects.get(pk=1)
        >>> # Assuming obj.first_name = 'John'
        >>> # Assuming obj.last_name = 'Doe'
        >>> obj_data = {
        >>>     'first_name': 'Jane',
        >>>     'last_name': 'Doe'
        >>> }
        >>> only_save_changed_data(obj, obj_data)
        ['first_name']

    Args:
        obj: The object/instance to work on
        obj_data: dict containing key: value where key is the attribute on the obj
        not_these_fields: Allows you to ignore/skip certain fields from obj_data
        not_these_fields_startswith: Same as not_these_fields but it does startswith on the obj_data keys
        save: Whether or not to actually save the obj. Supply False when you just want to know what changed.

    Returns:
        set containing fields that actually changed.
    """

    if not_these_fields is not None and not isinstance(not_these_fields, (list, tuple, set)):
        raise TypeError('param not_these_fields must be of type list, tuple, or set.')
    if not_these_fields_startswith is not None and not isinstance(not_these_fields_startswith, (list, tuple, set)):
        raise TypeError('param not_these_fields_startswith must be of type list, tuple, or set.')

    # Because there are so many rows, I only want to actually save when something has changed.
    changed = set()
    for field, data in obj_data.items():

        if not_these_fields and field in not_these_fields:
            continue

        elif not_these_fields_startswith:
            cont = False
            for f in not_these_fields_startswith:
                if field.lower().startswith(f.lower()):
                    cont = True
                    break
            if cont:
                continue

        # Ensure we have data and that it doesn't match what we already have
        if hasattr(obj, field) and getattr(obj, field) != data:
            changed.add(field)
            setattr(obj, field, data)

    if changed and save:
        obj.save(update_fields=changed)

    return changed


def get_app_name_for_queryset_filter():
    return get_param_name_for_queryset_filter('app')


def get_name_name_for_queryset_filter():
    return get_param_name_for_queryset_filter('name')


def get_param_name_for_queryset_filter(key: str):
    val = getattr(app_settings, f'SETTINGS_CASE_SENSITIVE_{key.upper()}')
    return key if val else f'{key}__iexact'
