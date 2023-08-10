from rest_framework import permissions

class AllowOnlyLabUsers(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "lab"
    
class AllowOnlyPatientUsers(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "patient"