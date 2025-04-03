from rest_framework.permissions import BasePermission

class CanDeleteDraftBill(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('master')
