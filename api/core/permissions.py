from rest_framework import permissions


class userprofile_permission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class wordlist_permission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.userprofile.user == request.user



class IsAdminOrIsSelf(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     if request.method == 'POST':
    #         return request.user.id == request.data["userprofile"]
    #     return True

    def has_object_permission(self, request, view, obj):
        # if request.method == 'POST':
        #     return request.user == request.data["userprofile"]
        return obj.userprofile.user == request.user #or request.user.is_staff or request.user.is_superuser

