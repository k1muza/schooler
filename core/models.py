import reversion
from django.db import models
from django.db.models.query import QuerySet
from reversion.models import Version


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


@reversion.register()
class VersionedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

    @property
    def versions(self) -> QuerySet[Version]:
        return Version.objects.get_for_object(self)

    def save(self, *args, **kwargs):
        with reversion.create_revision():
            super(VersionedModel, self).save(*args, **kwargs)
