from django.urls import path
from rest_framework import routers

from .views import PostViewSet, TaskViewSet, SubmissionViewSet, CompanyViewSet

app_name = "posts"

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename="post")
router.register(r'tasks', TaskViewSet, basename="task")
router.register(r'result', SubmissionViewSet, basename="result")
router.register(r'company', CompanyViewSet, basename="company")
urlpatterns = [

] + router.urls
