from django.db import models
from django.contrib.auth.models import AbstractUser

from iarp_django_utils.models import BaseSetting, CookieAutoLoginBaseFieldsModel, PageContentsBase


class TestModel(models.Model):
    name = models.CharField(max_length=50, blank=True)


class Setting(BaseSetting):
    pass


class User(AbstractUser, CookieAutoLoginBaseFieldsModel):
    pass


class PageContent(PageContentsBase):
    pass
