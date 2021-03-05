from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('api/docs/', get_swagger_view(title='CodeHive API')),
    path('admin/', admin.site.urls),
    path('api/', include('custom.urls', namespace="user-api")),
]
