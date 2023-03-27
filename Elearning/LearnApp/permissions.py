from rest_framework.permissions import BasePermission

from LearnApp.models import User


class AdminsPermissions(BasePermission):
    allowed_user_roles = User.role

    def has_permission(self, request, view):
        is_allowed_user = request.user.role in self.allowed_user_roles
        return is_allowed_user