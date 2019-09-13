import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer,
    RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer,
)
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import refresh_jwt_token

from apps.api.v1.permissions import ObjectPermissions
from apps.api.v1.serializers import BadRequestResponseSerializer, CommonErrorResponseSerializer
from apps.api.v1.serializers.accounts import (
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    UserChangePasswordSerializer,
    UserFullSerializer,
    UserLoginResponseSerializer,
    UserRegistrationSerializer,
)
from apps.api.v1.tokens import EmailVerifyTokenGenerator, PasswordResetTokenGenerator
from apps.api.v1.viewsets import ExtendedModelViewSet
from apps.notifications.tasks import send_templated_email

User = get_user_model()
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class UserViewSet(ExtendedModelViewSet):
    """
    View for working with user data.

    retrieve:
    Return the given user.

    list:
    List all users.

    update:
    Update user data.

    partial_update:
    Partial update user data.

    delete:
    Mark user as deleted.
    """

    queryset = User.objects.all()
    serializer_class = UserFullSerializer
    serializer_class_map = {
        'login': JSONWebTokenSerializer,
        'refresh': RefreshJSONWebTokenSerializer,
        'verify': VerifyJSONWebTokenSerializer,
        'registration': UserRegistrationSerializer,
        'change_password': UserChangePasswordSerializer,
        'password_reset': PasswordResetSerializer,
        'password_reset_confirm': PasswordResetConfirmSerializer,
    }
    permission_map = {
        'login': permissions.AllowAny,
        'refresh': permissions.IsAuthenticated,
        'verify': permissions.IsAuthenticated,
        'registration': permissions.AllowAny,
        'verify_email': permissions.AllowAny,
        'send_verify_email': permissions.AllowAny,
        'password_reset': permissions.AllowAny,
        'password_reset_confirm': permissions.AllowAny,
    }
    permission_classes = (ObjectPermissions,)

    def _auth(self, request, serializer):
        if serializer.is_valid(raise_exception=True):
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = timezone.now() + api_settings.JWT_EXPIRATION_DELTA
                response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
            return response

    @swagger_auto_schema(
        responses={
            200: UserLoginResponseSerializer,
            400: BadRequestResponseSerializer,
            410: BadRequestResponseSerializer,
        }
    )
    @action(methods=['post'], detail=False)
    def login(self, request):
        """
        Retrieve auth token by pair of username & password.
        """
        serializer = self.get_serializer(data=request.data)
        return self._auth(request, serializer)

    @swagger_auto_schema(
        responses={
            200: UserLoginResponseSerializer,
            400: BadRequestResponseSerializer,
            410: BadRequestResponseSerializer,
        }
    )
    @action(methods=['post'], detail=False)
    def refresh(self, request):
        """
        Refresh auth token by exist.
        """
        serializer = self.get_serializer(data=request.data)
        return self._auth(request, serializer)

    @swagger_auto_schema(
        responses={
            200: UserLoginResponseSerializer,
            400: BadRequestResponseSerializer,
            410: BadRequestResponseSerializer,
        }
    )
    @action(methods=['post'], detail=False)
    def verify(self, request):
        """
        Verify auth token by exist.
        """
        serializer = self.get_serializer(data=request.data)
        return self._auth(request, serializer)

    @swagger_auto_schema(responses={201: UserFullSerializer, 400: BadRequestResponseSerializer})
    @action(methods=['post'], detail=False)
    def registration(self, request):
        """
        Register user with first_name, last_name, email, phone, password1, password2 fields.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            self._send_verify_email(request, user)
            data = UserFullSerializer(instance=user).data
            return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False)
    def me(self, request, pk=None, **kwargs):
        """
        Retrieve logged user information.
        """
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={
            200: UserChangePasswordSerializer,
            400: BadRequestResponseSerializer,
            410: BadRequestResponseSerializer,
        }
    )
    @action(methods=['post'], detail=False, url_path='change-password')
    def change_password(self, request):
        """
        Change password.
        """
        serializer = self.get_serializer(data=request.data, instance=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = UserFullSerializer(instance=request.user).data
            return Response(data)

    @swagger_auto_schema(responses={200: serializers.Serializer, 400: BadRequestResponseSerializer})
    @action(methods=['get'], detail=True, url_path=r'verify-email/(?P<key>[^/.]+)')
    def verify_email(self, request, pk=None, key=None, **kwargs):
        """
        Verify user email.
        """
        user = self.get_object()
        is_valid_token = EmailVerifyTokenGenerator().check_token(user, key)
        if is_valid_token:
            user.is_email_proved = True
            user.save()
            return Response()
        else:
            return Response({'errors': {'token': _('Not valid email token')}}, status=status.HTTP_400_BAD_REQUEST)

    def _send_verify_email(self, request, user):
        key = EmailVerifyTokenGenerator().make_token(user)
        refferer = request.META.get('HTTP_HOST')
        # TODO: Need specify uri!
        path = reverse('api_v1:api-root:accounts-verify-email', kwargs={'pk': user.id, 'key': key})
        url = f'https://{refferer}{path}'
        send_templated_email.delay(_('Verify your email'), user.email, 'notifications/verify_email.html', url=url)

    def _password_generator(self, size=8, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for i in range(size))

    @swagger_auto_schema(responses={200: serializers.Serializer, 400: BadRequestResponseSerializer})
    @action(
        methods=['get'], detail=False, url_path=r'send-verify-email/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})'
    )
    def send_verify_email(self, request, email=None, **kwargs):
        """
        Send verify user email.
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            data = {'errors': {'email': _('user not registered')}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            self._send_verify_email(request, user)
            return Response()

    @action(methods=['post'], detail=False)
    def password_reset(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def password_reset_confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
