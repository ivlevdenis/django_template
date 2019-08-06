import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import DeletedManager, UserDeletedManager


class UUIDModel(models.Model):
    id = models.UUIDField(_('ID'), default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        abstract = True


class DeletedModel(models.Model):
    deleted_at = models.DateTimeField(_('deleted at'), null=True, blank=True, editable=False)

    objects = DeletedManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()
            self.save()


class UserDeletedModel(models.Model):
    deleted_at = models.DateTimeField(_('deleted at'), null=True, blank=True, editable=False)

    objects = UserDeletedManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()
            self.save()


class CreatedDeletedModel(CreatedModel, DeletedModel):
    class Meta:
        abstract = True
