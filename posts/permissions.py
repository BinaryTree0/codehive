from rest_framework.permissions import BasePermission


class IsListDetailOrIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == 'list' and view.action == "retrieve":
                return True
            else:
                return False
        else:
            return True
