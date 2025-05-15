from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
       
        if request.user.is_superuser:
            return True

        return obj.owner==request.user 

class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.owner==request.user
      