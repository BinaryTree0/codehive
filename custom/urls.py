from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import ActivateView, ActivateConfirmView, ResetView, ResetConfirmView, UserViewSet, ChangePasswordView

app_name = "custom"

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path("users/<int:uid>/password", ChangePasswordView.as_view(), name="change"),
    path('users/login', views.obtain_auth_token, name="login"),
    path('users/password-reset', ResetView.as_view(), name="reset"),
    path('users/password-reset-confirm', ResetConfirmView.as_view(), name="reset-confirm"),
    path('users/account-activate', ActivateView.as_view(), name="activate"),
    path('users/account-activate-confirm', ActivateConfirmView.as_view(), name="activate-confirm"),
] + router.urls
