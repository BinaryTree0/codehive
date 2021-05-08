from django.urls import path
from rest_framework_nested import routers

from .views import (CompanyViewSet, InstitutionViewSet,
                    PostViewSet, ProfileEducationViewSet,
                    ProfileExperienceViewSet, ProfileSkillViewSet,
                    ProfileViewSet, SkillViewSet, SubmissionViewSet,
                    TaskUserViewSet, TaskViewSet, TestFileUploadViewSet)

app_name = "posts"

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename="post")
router.register(r'tasks', TaskViewSet, basename="task")
router.register(r'submissions', SubmissionViewSet, basename="submissions")
router.register(r'companies', CompanyViewSet, basename="companies")
router.register(r'institutions', InstitutionViewSet, basename="institutions")
router.register(r'profiles', ProfileViewSet, basename="profiles")
router.register(r'skills', SkillViewSet, basename="skills")
router.register(r'task-users', TaskUserViewSet, basename="task-users")
router.register(r'file-upload', TestFileUploadViewSet, basename="file-upload")


profile_router = routers.NestedSimpleRouter(router, r'profiles', lookup='profile')
profile_router.register(r'education', ProfileEducationViewSet, basename='profile-education')
profile_router.register(r'experiences', ProfileExperienceViewSet, basename="profile-experiences")
profile_router.register(r'skills', ProfileSkillViewSet, basename="profile-skills")

urlpatterns = [

] + router.urls + profile_router.urls
