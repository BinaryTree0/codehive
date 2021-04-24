from django.urls import path
from rest_framework import routers

from .views import PostViewSet, TaskViewSet, SubmissionViewSet, CompanyViewSet, \
    ProfileViewSet, InstitutionViewSet, SkillViewSet

app_name = "posts"

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename="post")
router.register(r'tasks', TaskViewSet, basename="task")
router.register(r'submissions', SubmissionViewSet, basename="submissions")
router.register(r'companies', CompanyViewSet, basename="companies")
router.register(r'institutions', InstitutionViewSet, basename="institutions")
router.register(r'profiles', ProfileViewSet, basename="profiles")
router.register(r'skills', SkillViewSet, basename="skills")
urlpatterns = [

] + router.urls
