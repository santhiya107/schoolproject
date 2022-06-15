from rest_framework.permissions import BasePermission

class IsStaffUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and (request.user.user_type == 'is_staff') )

class IsAdminUser(BasePermission):

    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and (request.user.user_type == 'is_admin'))
