from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Class to check permissions of a user to modify a post"""

    message = "Not the author"

    def has_object_permission(self, request, view, post):
        """Check if the method is safe (read-only) or if the user is authorized to modify the post"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == post.author


class IsFollower(permissions.BasePermission):
    """Class to check permissions of a user to delete their followers"""

    message = "Not a follower"

    def has_object_permission(self, request, view, user_follower):
        """Check if the user is authorized to delete their followees"""
        if request.method == "DELETE":
            return request.user == user_follower.follower
        return True
