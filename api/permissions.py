from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.role == 'admin'

class IsAdminSave(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS \
               or request.user.is_staff \
               or request.user.role == 'admin'

class ReviewAndComment(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        elif request.method == 'PATCH':
            return True
        elif request.method == 'DELETE':
            return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method == 'PATCH' or request.method == 'DELETE':
            return obj.author == request.user or request.user.role in [
                'moderator', 'admin']



