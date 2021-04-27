from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('api/docs/', get_swagger_view(title='CodeHive API')),
    path('admin/', admin.site.urls),
    path('api/', include('custom.urls', namespace="user-api")),
    path('api/', include('posts.urls', namespace="post-api")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
