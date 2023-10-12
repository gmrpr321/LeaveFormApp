from rest_framework import permissions

class StudentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

class StaffPermissions(permissions.BasePermission):
    pass

class HODPermissions(permissions.BasePermission):
    pass

