from django.contrib.auth import models as auth_models
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.models import UserDeletedModel


class User(UserDeletedModel, auth_models.AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30)
    middle_name = models.CharField(_('middle name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150)
    phone = PhoneNumberField(_('phone'), null=True, blank=True, unique=True)
    email = models.EmailField(_('email address'), unique=True, null=True)
    is_agree_with_agreement = models.DateTimeField(_('is agree with user agreement'), null=True, blank=True)
    is_phone_proved = models.BooleanField(_('is phone proved'), default=False)
    is_email_proved = models.BooleanField(_('is email proved'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(auth_models.AbstractUser.Meta):
        ordering = ('email',)
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        indexes = (models.Index(fields=('email',)),)

    def __str__(self):
        return self.email
