import copy

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginator_helper(context_key, queryset, requested_page=None, limit=None, params=None,
                     page_url_param=getattr(settings, 'PAGINATION_PAGE_PARAM', 'page'),
                     limit_url_param=getattr(settings, 'PAGINATION_LIMIT_PARAM', 'limit'),
                     last_first=getattr(settings, 'PAGINATION_LAST_FIRST', False), **kwargs):
    """ Builds and supports the custom pagination system this system uses.

    Examples:

        Standard Template and View usage:
            {% include 'core/pagination.html' %}

            def get_context_data(self, **kwargs):
                kwargs.update(paginator_helper(
                    context_key='images',
                    queryset=self.object.images.all(),
                    params=self.request.GET,
                ))
                return super().get_context_data(**kwargs)

        Custom Page and Limit Template and View usage:
            {% include 'core/pagination.html' with page_url_param='comments_page' limit_url_param='comments_limit' %}

            def get_context_data(self, **kwargs):
                kwargs.update(paginator_helper(
                    context_key='images',
                    queryset=self.object.images.all(),
                    page_url_param='comments_page',
                    limit_url_param='comments_limit',
                    params=self.request.GET,
                ))
                return super().get_context_data(**kwargs)

    Args:
        context_key: The objects list key passed into the template context
        queryset: The queryset to base pagination on
        requested_page: Which page to load
        limit: How many items per page
        params: Typically just request.GET, it fixes the url to allow
            extra GET parameters and not interfere with ?page mechanism.
        page_url_param: The param to be found in params that
            pertains to the page being loaded.
        limit_url_param: The param to be found in params that
            pertains to the number of items returned per page.
        last_first: Whether or not to load the first or last page
            when no page param is given.

    Returns:
        dict of data to be added to the templates context for pagination purposes.
    """
    if not isinstance(params, dict):
        params = {}
    if page_url_param and page_url_param in params:
        requested_page = params[page_url_param]
        last_first = False
    if limit_url_param and limit_url_param in params:
        limit = params[limit_url_param]

    if last_first and requested_page is None:
        requested_page = -1
    else:
        requested_page = requested_page or 1

    paginator = Paginator(
        object_list=queryset,
        per_page=limit or 15,
        **kwargs
    )

    try:
        page = paginator.page(requested_page)
    except (EmptyPage, PageNotAnInteger):
        try:
            requested_page = int(requested_page)
            if requested_page == -1 or requested_page > paginator.num_pages:
                requested_page = paginator.num_pages
            elif requested_page <= 0:
                raise ValueError
        except (ValueError, TypeError):
            requested_page = 1

        page = paginator.page(requested_page)

    base_url = ''
    if params and isinstance(params, dict):
        params = copy.deepcopy(params)
        if page_url_param in params:
            del params[page_url_param]
        result = []
        for k, v in params.items():
            result.append(f'{k}={v}')
        result = '&'.join(result)
        if result:
            base_url = f'{result}&'

    return {
        context_key: page.object_list,
        'paginator': paginator,
        'page_obj': page,
        'pagination_base_url': f'?{base_url}',
        'is_paginated': paginator.num_pages > 1,
    }
