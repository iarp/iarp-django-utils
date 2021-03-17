=====================
IARP Django Utilities
=====================

A collection of django utilities I use a lot throughout many projects.

I only work with Python 3.6 and 3.7 currently, as such these may not work in
previous versions. Most notably due to f-strings.

Installation
============

    pip install -e git+https://iarp@bitbucket.org/iarp/iarp-django-utils.git#egg=iarp_django_utils

Add the following to settings.py::

    INSTALLED_APPS = [
        ...
        'iarp_django_utils',
        ...
    ]

Documentation
=============

Every file and function is commented about what it does, how and when to use
it along with examples. Have a question? Open an issue.


Pagination
==========

Add the following to settings.py::

    TEMPLATES = [
        {
            ...
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    ...
                    'iarp_django_utils.template_contexts.add_pagination_settings',
                ],
            },
        },
    ]

Anywhere you wish to include pagination use the following in your template where ever you wish for the pagination to appear::

    {% include 'iarp_django_utils/pagination.html' %}

Pagination Settings
-------------------

PAGINATION_INCLUDE_SEPARATOR (=None)
    What value to use as a separator when there are more pages than can comfortably be displayed.

PAGINATION_INCLUDE_FIRST (=None)
    Do you always want to show the first X number of pages?

    if pagination_include_first == 3 and current_page = 57, output will look like:
        1, 2, 3, ..., 56, 57, 58

PAGINATION_INCLUDE_LAST (=0)
    Do you always want to show the last X number of pages?

    if pagination_include_last == 3 and current_page == 57, output will look like:
        First, Prev, 56, 57, 58, ..., 97, 98, 99, Next, Last

PAGINATION_NEIGHBORS (=4)
    How many neighbouring pages to include around the current page.

    if pagination_neighbors == 2 and current_page == 34, output will look like:
        First, Prev, 32, 33, 34, 35, 36, Next, Last

PAGINATION_BUTTON_CLASSES (='btn btn-sm btn-secondary')
    What classes to set the First/Next/Last/Prev buttons

PAGINATION_INCLUDE_LAST_PAGE_IN_LAST_BUTTON (=True)
    Do you want to show the maximum number of pages on the Last button?

    if True output looks like:
        Last (96) >>
    else:
        Last >>

Cookie Auto Login
=================

Built for my grandmother. Use an addon in your browser that has the ability
to protect cookies from deletion/modification.

Installation
------------

Requires a custom user model to be used.

::

    MIDDLEWARE = [
        ...,
        'iarp_django_utils.middleware.cookie_login.CookieAutoLogin',
    ]

Inherit from `iarp_django_utils.models.CookieAutoLoginBaseFieldsModel` on your user model.

Cookie Settings
---------------

COOKIE_LOGIN_KEY (required)
    The name of the cookie to look for and compare passworded values.

COOKIE_LOGIN_AUTH (='')
    String path to a function that accepts `user, cookie_value, request`.
    Return True/False if the cookie_value is correct for the user supplied.

    If returned True, it will login the user.

COOKIE_LOGIN_BACKEND (="django.contrib.auth.backends.ModelBackend")
    What backend to use logging in the user.
