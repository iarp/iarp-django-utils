from django.conf import settings


def add_pagination_settings(request=None):
    return {
        'pagination_include_separator': getattr(settings, 'PAGINATION_INCLUDE_SEPARATOR', None),
        'pagination_include_first': getattr(settings, 'PAGINATION_INCLUDE_FIRST', None),
        'pagination_include_last': getattr(settings, 'PAGINATION_INCLUDE_LAST', None),
        'pagination_neighbors': getattr(settings, 'PAGINATION_NEIGHBORS', None),
        'pagination_button_classes': getattr(settings, 'PAGINATION_BUTTON_CLASSES', 'btn btn-sm btn-secondary'),
        'pagination_include_last_page_in_last_button': getattr(settings, 'PAGINATION_INCLUDE_LAST_PAGE_IN_LAST_BUTTON', True),
    }
