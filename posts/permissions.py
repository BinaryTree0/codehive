from rest_framework.permissions import BasePermission

from .models import Company


class IsListDetailOrIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == 'list' or view.action == "retrieve":
                return True
            else:
                return False
        else:
            return True


class isOwner(BasePermission):

    def has_permission(self, request, view):
        print(request)
        if not request.user.is_authenticated:
            if view.action == 'list' or view.action == "retrieve":
                return True
            else:
                return False
        else:
            return True


class IsCompany(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.user.is_company:
            if view.action == 'list' or view.action == "retrieve":
                return True
            else:
                return False
        else:
            return True
