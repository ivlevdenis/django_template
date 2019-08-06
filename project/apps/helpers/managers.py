from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.utils import timezone


class DeletedQueryMixin(models.query.QuerySet):
    def delete(self, force=False):
        if force:
            return super().delete()
        else:
            return self._delete()

    def _delete(self):
        return (
            self.count(),
            self.update(deleted_at=timezone.now())
        )

    def deleted(self):
        return self.filter(deleted_at__isnull=False)

    def non_deleted(self):
        return super().filter(deleted_at__isnull=True)


class DeletedQuerySet(DeletedQueryMixin, models.query.QuerySet):
    pass


class DeletedManager(models.Manager):
    def get_queryset(self):
        return DeletedQuerySet(self.model, using=self._db)

    def deleted(self):
        return self.get_queryset().deleted()

    def non_deleted(self):
        return self.get_queryset().non_deleted()


class UserDeletedManager(DeletedManager, BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=self.normalize_email(email),
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
