from django.db import models
from django.urls import reverse


class Item(models.Model):
    body = models.TextField()

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('demo:item-detail', args=[self.pk])


class SubItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='subitems')
    body = models.TextField()

    def __str__(self):
        return self.body
