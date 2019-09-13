import base64
import imghdr
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator, ValidationError


User = get_user_model()


class UserFullSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'phone',
            'email',
        )
        read_only_fields = ('id', 'phone', 'email')


class UserLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(User.objects.all())], required=False)
    is_agree_with_agreement = serializers.NullBooleanField()

    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate_password2(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError(detail=_('Passwords does not match'))
        return super().validate(attrs)

    def create(self, validated_data):
        username = validated_data.get(User.USERNAME_FIELD)
        is_agree_with_agreement = validated_data.get('is_agree_with_agreement')
        user = User.objects.create(
            username=username,
            email=validated_data.get('email'),
            is_agree_with_agreement=timezone.now() if is_agree_with_agreement else None,
        )
        user.set_password(validated_data.get('password2'))
        user.save()
        return user


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        return self.instance

    def validate_password(self, value):
        if not self.instance.check_password(value):
            raise ValidationError(detail=_('Passwords does not correct'))
        return value

    def validate_password1(self, value):
        validate_password(value)
        return value

    def validate_password2(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError(detail=_('Passwords does not match'))
        return super().validate(attrs)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise exceptions.ValidateError(_(f'User with email {value} not found.'))
        return value

    def save(self):
        request = self.context.get('request')
        email = request.data['email']
        user = User.objects.get(email__iexact=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)
        url = f'{settings.SITE_URL}/restore/{uid}/{token}'
        context = {'email': email, 'url': url}
        body = loader.render_to_string('password_reset.html', context=context)
        send_mail('{{ project_name }} Platform Password Reset', body, None, (user.email,))


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(allow_blank=False)
    token = serializers.CharField(allow_blank=False)
    password1 = serializers.CharField(allow_blank=False, max_length=128)
    password2 = serializers.CharField(allow_blank=False, max_length=128)

    def validate(self, attrs):
        try:
            uid = force_text(urlsafe_base64_decode(attrs['uid']))
            self.user = User.objects.get(pk=uid)
        except (ValueError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({'password2': ['Passwords do not match']})
        validate_password(attrs['password2'], self.user)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})
        return attrs

    def save(self):
        password1 = self.validated_data['password1']
        self.user.set_password(password1)
        self.user.save()
        return self.user
