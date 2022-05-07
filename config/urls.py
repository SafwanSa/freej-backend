from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="freej API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@freej.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

API_VERSION = 'v1'
urlpatterns = [
    path(f'api/{API_VERSION}/auth/', include('apps.account.urls')),
    path(f'api/{API_VERSION}/campuses/', include('apps.campus.urls')),
    path(f'api/{API_VERSION}/announcements/', include('apps.announcement.urls')),
    path(f'api/{API_VERSION}/events/', include('apps.event.urls')),
    path(f'api/{API_VERSION}/posts/', include('apps.post.urls')),
    path(f'api/{API_VERSION}/notifications/', include('apps.notification.urls')),
    path(f'api/{API_VERSION}/reports/', include('apps.report.urls')),
    path(f'api/{API_VERSION}/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]
