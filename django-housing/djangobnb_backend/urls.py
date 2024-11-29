from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Configuration de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Django API",
        default_version='v1',
        description="Documentation de l'API pour le projet Django",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/properties/', include('property.urls')),
    path('api/auth/', include('useraccount.urls')),
    # Ajouter Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='swagger-json'),  # Optional: Swagger JSON
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)