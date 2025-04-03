from rest_framework.permissions import BasePermission

class CanDeleteContributions(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('contribution')
