from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.response import Response


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if AnonymousUser:
            return Response({'123'}, status=400)
        return request.user.role == 'admin'

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator'
