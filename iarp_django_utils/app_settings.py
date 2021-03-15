class AppSettings(object):
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, default):
        from django.conf import settings

        return getattr(settings, f'{self.prefix}{name}', default)

    @property
    def SETTINGS_USE_HOSTNAME_SEPARATION(self):
        """
        Controls whether or not to use the hostname value on BaseSetting
        """
        return self._setting('SETTINGS_USE_HOSTNAME_SEPARATION', True)

    @property
    def SETTINGS_BLANK_HOSTNAME_IS_DEFAULT(self):
        """
        If the hostname specific setting does not exist, should we check
        for a hostname='' entry and use that as the default?
        """
        return self._setting('SETTINGS_BLANK_HOSTNAME_IS_DEFAULT', True)

    @property
    def SETTINGS_CASE_SENSITIVE_NAME(self):
        return self._setting('SETTINGS_CASE_SENSITIVE_NAME', True)

    @property
    def SETTINGS_CASE_SENSITIVE_APP(self):
        return self._setting('SETTINGS_CASE_SENSITIVE_APP', True)


app_settings = AppSettings('IARPDJANGOUTILS_')
