from django.urls import path
from rest_framework import routers

from .views import PostViewSet, TaskViewSet, ResultViewSet

app_name = "posts"

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename="post")
router.register(r'tasks', TaskViewSet, basename="task")
router.register(r'result', ResultViewSet, basename="result")
urlpatterns = [

] + router.urls
