from django.urls import path
from rest_framework import routers

from .views import PostViewSet

app_name = "posts"

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename="post")

urlpatterns = [

] + router.urls
