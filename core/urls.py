from django.contrib import admin
from django.http import HttpResponseNotFound
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('product/', include('product.urls')),
    path('basket/', include('basket.urls'))
]

def page_not_found(request, exception):
    text = ("<h1>Page not found<br>"
            "please include in this urls:<br>"
            "swagger/<br>"
            "admin/<br>"
            "user/<br>"
            "product/<br>"
            "basket/</h1>")

    return HttpResponseNotFound(text)

handler404 = page_not_found