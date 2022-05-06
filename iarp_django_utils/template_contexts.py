from django.conf import settings


def add_pagination_settings(request=None):
    return {
        'pagination_include_separator': getattr(settings, 'PAGINATION_INCLUDE_SEPARATOR', None),
        'pagination_include_first': getattr(settings, 'PAGINATION_INCLUDE_FIRST', None),
        'pagination_include_last': getattr(settings, 'PAGINATION_INCLUDE_LAST', None),
        'pagination_neighbors': getattr(settings, 'PAGINATION_NEIGHBORS', None),
        'pagination_include_last_page_in_last_button': getattr(
            settings, 'PAGINATION_INCLUDE_LAST_PAGE_IN_LAST_BUTTON', True
        ),
        'pagination_ul_class': getattr(settings, 'PAGINATION_UL_CLASS', 'pagination justify-content-center flex-wrap'),
        'pagination_li_class': getattr(settings, 'PAGINATION_LI_CLASS', 'page-item'),
        'pagination_li_disabled_class': getattr(settings, 'PAGINATION_LI_DISABLED_CLASS', 'page-item disabled'),
        'pagination_li_a_class': getattr(settings, 'PAGINATION_LI_A_CLASS', 'page-link'),
        'pagination_li_span_class': getattr(settings, 'PAGINATION_LI_SPAN_CLASS', 'page-link'),
    }
