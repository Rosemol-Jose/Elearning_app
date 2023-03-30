from rest_framework.permissions import BasePermission

from LearnApp.models import User


class IsStudent(BasePermission):

    permissions=False
    def has_permission(self, request, view):

        if request.user.role == 'student' or request.user.role == 1:
            permissions=True
        return permissions


class IsTeacher(BasePermission):

    permissions=False
    def has_permission(self, request, view):

        if request.user.role == 'teacher' or request.user.role == 2:
            permissions=True
        return permissions
class IsOwner(BasePermission):
    #if a teacher is owner to the course

    def has_object_permission(self, request, view, obj):
        # Permissions are only allowed to the owner of the snippet
        return obj.added_by == request.user

