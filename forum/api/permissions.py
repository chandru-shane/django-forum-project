from rest_framework import permissions

class IsCreatedUser(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_user == request.user 
