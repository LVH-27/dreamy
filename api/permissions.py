from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Class to check permissions of a user to modify a post"""

    message = "Not the author"

    def has_object_permission(self, request, view, post):
        """Check if the method is safe (read-only) or if the user is authorized to modify the post."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == post.author
