import django


if django.VERSION < (4, 0):
    default_app_config = "iarp_django_utils.apps.IarpDjangoUtilsConfig"
