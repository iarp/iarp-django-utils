from django.db import models
from iarp_django_utils.models import BaseSetting


class TestModel(models.Model):
    name = models.CharField(max_length=50, blank=True)


class Setting(BaseSetting):
    pass
