from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path, include
from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title="Pay Up Backend REST API",
        default_version='Version 1.6',
        description="Car Pool App API\n\n **By Team RAGS** \n\n~ Powered by django-rest-framework\n\n",
        contact = openapi.Contact("Team Rags Team", "https://github.com/R-AG-S", "sandeep.pillai42@gmail.com")

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('carpool/', include('carpool.urls')),
    path('active/', include('active_carpool.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),

    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    path("redoc", schema_view.with_ui('redoc',
                                      cache_timeout=0), name='schema-redoc'),
]