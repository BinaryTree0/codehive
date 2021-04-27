from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (ActivateConfirmView, ActivateView, ChangePasswordView,
                    ObtainAuthTokenWithActivation, ResetConfirmView, ResetView,
                    UserViewSet)

app_name = "custom"

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="user")

urlpatterns = [
    path("users/<int:id>/password", ChangePasswordView.as_view(), name="password-change"),
    path('users/password-reset', ResetView.as_view(), name="password-reset"),
    path('users/password-reset-confirm', ResetConfirmView.as_view(), name="password-reset-confirm"),
    path('users/login', ObtainAuthTokenWithActivation.as_view(), name="user-login"),
    path('users/account-activate', ActivateView.as_view(), name="user-activate"),
    path('users/account-activate-confirm', ActivateConfirmView.as_view(), name="user-activate-confirm"),
] + router.urls
