import base64
import datetime
import socket
import warnings

from django.db import models

from iarp_utils.datetimes import fromisoformat
from iarp_utils.strings import startswith_many
from .app_settings import app_settings
from iarp_django_utils import helpers


class BaseSetting(models.Model):

    class Meta:
        abstract = True
        unique_together = ['app', 'name', 'hostname']
        ordering = ['app', 'name', 'hostname']

    app = models.CharField(max_length=255, help_text='Typically the app it belongs to i.e. games')
    name = models.CharField(max_length=255, help_text='Name that corresponds to the value stored i.e. username')
    hostname = models.CharField(max_length=255, default='', blank=True, help_text='Name of the computer this setting is specific to.')
    value = models.TextField(blank=True)

    inserted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.app}.{self.name}={self.value}'

    @staticmethod
    def _get_hostname(system_specific=False, hostname=''):

        if not app_settings.SETTINGS_USE_HOSTNAME_SEPARATION:
            return ''

        if system_specific:
            hostname = socket.gethostname().lower()

        return hostname.replace('.', '')

    @classmethod
    def get_value(cls, name, app=None, default=None, **kwargs):
        """ Returns a single value for the name and app supplied.
        Name can also be dot notation i.e. system.domain_root

        Examples:

            >>> BaseSetting.get_value('Games.api_key')
            fas9k2ldas76dg

            >>> BaseSetting.get_value('Games.SeasonId', default=18)
            18

        Args:
            name: Settings name value
            app: The application the setting is for
            default: if a value is not found in the database, return this default value.
            system_specific: Whether or not the setting is specific based on hostname.
            hostname: The hostname to use if you don't want to use the current machines name.
            kwargs: Only here for backwards compatibility

        Returns:
            Gets the value for given app and name.
        """
        if not app:
            app, name = name.split('.', 1)

        hostname = cls._get_hostname(**kwargs)

        app_key = helpers.get_app_name_for_queryset_filter()
        name_key = helpers.get_name_name_for_queryset_filter()

        query_params = {
            app_key: app,
            name_key: name,
            'hostname': hostname,
        }

        try:
            s = cls.objects.get(**query_params)
        except cls.DoesNotExist:

            # If the setting for this specific hostname was not found, look for a default which
            # has no hostname and use that.
            if hostname and default is None and app_settings.SETTINGS_BLANK_HOSTNAME_IS_DEFAULT:

                try:
                    s = cls.objects.get(**query_params)
                except cls.DoesNotExist:
                    s = None
                except cls.MultipleObjectsReturned:
                    warnings.warn(f'Settings {app}.{name} hm="" returned multiple items!')
                    s = cls.objects.filter(app=app, name=name, hostname='').order_by('-last_updated').first()

                if s:
                    default = s.value

            s = cls.objects.create(
                app=app, name=name, value=str(default if default is not None else ''),
                hostname=hostname,
            )
        except cls.MultipleObjectsReturned:
            warnings.warn(f'Settings {app}.{name} hm={hostname} returned multiple items!')
            s = cls.objects.filter(app=app, name=name, hostname=hostname).order_by('-last_updated').first()
        except:
            return default

        value = s.value

        dts = ['date||', 'datetime||']
        if startswith_many(value, dts):
            for t in dts:
                if value.startswith(t):
                    value = value.replace(t, '')
                    try:
                        value = fromisoformat(value)
                        if t == 'date||':
                            return value.date()
                        return value
                    except ValueError:
                        pass
                    finally:
                        break

        if value.lower() in ['true', 'false']:
            return value.lower() == 'true'

        if value.isdigit():
            return int(value)

        if name.strip().lower() == 'password':
            return cls._decode_value(value)

        return value

    @classmethod
    def set_value(cls, name, app=None, value=None, **kwargs):
        """ Sets a value for the name and app supplied.
        Name can also be dot notation i.e. system.domain_root

        Args:
            name: Settings name value
            app: The application the setting is for
        """
        if not app:
            app, name = name.split('.', 1)

        hostname = cls._get_hostname(**kwargs)

        if isinstance(value, datetime.datetime):
            value = f'datetime||{value.isoformat()}'
        elif isinstance(value, datetime.date):
            value = f'date||{value.isoformat()}'
        elif name.strip().lower() == 'password':
            try:
                obj = cls.objects.get(app=app, name=name, hostname=hostname)
            except cls.DoesNotExist:
                obj = None

            if not obj or obj.value != value:
                value = cls._encode_value(value)

        s, _ = cls.objects.update_or_create(app=app, name=name, hostname=hostname, defaults={'value': value})
        return s

    @staticmethod
    def _decode_value(value):
        return base64.b64decode(value).decode('utf-8')

    @staticmethod
    def _encode_value(value):
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')
