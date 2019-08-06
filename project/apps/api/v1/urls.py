from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from apps.api.v1.views.accounts import OrganizationViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'accounts', UserViewSet, basename='accounts')


schema_view = get_schema_view(
    openapi.Info(title='{{ project_name }} API', default_version='v1', description='Routes of {{ project_name }} project'),
    # validators=['flex', 'ssv'],
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger(<str:format>.json|.yaml)', schema_view.without_ui(), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc'), name='schema-redoc'),
    path('', include((router.urls, 'api-root')), name='api-root'),
]
