from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import ActivateView, ActivateConfirmView, ResetView, ResetConfirmView, UserViewSet

app_name = "custom"

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('users/login', views.obtain_auth_token, name="login"),
    path('users/reset', ResetView.as_view(), name="reset"),
    path('users/reset-confirm', ResetConfirmView.as_view(), name="reset-confirm"),
    path('users/activate', ActivateView.as_view(), name="activate"),
    path('users/activate-confirm', ActivateConfirmView.as_view(), name="activate-confirm"),
] + router.urls
