from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone


def delete_relationshiped_items(obj):
    """Deletes all relationshiped objects.

        Since this system doesn't actually delete rows, on_delete=models.CASCADE won't do anything.
        We have to re-create that CASCADE action.

    :param data:
    :return:
    """
    for field in obj._meta.get_fields():

        # Since we're not actually deleting rows, issue .delete() on
        # all related items as CASCADE won't actually cascade
        # since we're just updating the deleted column.
        if getattr(field, 'on_delete', None) == models.CASCADE:

            if type(field) in [models.ManyToOneRel, models.ManyToManyRel]:

                # Filtering doesn't require catching an exception
                getattr(obj, field.get_accessor_name()).all().delete()

            elif type(field) == models.OneToOneRel:

                # OneToOne accessing the other object directly,
                # calling .delete raises model.DoesNotExist
                # Need to catch the base exception.
                try:
                    getattr(obj, field.get_accessor_name()).delete()
                except (ObjectDoesNotExist, AttributeError):
                    pass


class DeactivateQuerySet(models.query.QuerySet):
    """QuerySet whose delete() does not delete items, but instead
    updates the deleted with a datetime value."""

    def delete(self):
        # for item in self.all():
        #     delete_relationshiped_items(item)
        self.update(deleted=timezone.now())


class DeactivateManager(models.Manager):
    """ Manager that returns a DeactivateQuerySet, to prevent object deletion. """

    def get_queryset(self):
        return DeactivateQuerySet(self.model, using=self._db).filter(deleted__isnull=True)


class DeactivateMixin(models.Model):
    """
    abstract class for models whose rows should not be deleted but
    items should be 'deactivated' instead.

    note: needs to be the first abstract class for the default objects
    manager to be replaced on the subclass.
    """

    objects = DeactivateManager()
    direct = models.Manager()

    deleted = models.DateTimeField(default=None, editable=False, null=True)

    class Meta:
        abstract = True

    def delete(self, full_delete=False, *args, **kwargs):

        if full_delete:
            return super().delete(*args, **kwargs)

        # delete_relationshiped_items(self)

        self.deleted = timezone.now()
        self.save()
