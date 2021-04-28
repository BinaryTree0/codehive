from rest_framework import permissions
from rest_framework.permissions import BasePermission

from .models import Company


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CreateOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return True
        else:
            return False


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        else:
            return True


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsProfileOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user


class IsPostOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.post.profile.user == request.user


class IsCompanyOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.company.user == request.user


class IsCompany(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_company:
            return True
        else:
            return False


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False
