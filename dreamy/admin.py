from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import UserFollower, Post
from .forms import DreamyUserCreationForm, DreamyUserChangeForm


User = get_user_model()


class DreamyUserAdmin(UserAdmin):
    """This class overrides the default UserAdmin to reflect the overridden User model"""

    add_form = DreamyUserCreationForm
    form = DreamyUserChangeForm
    # model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'avatar',)}),
    )


admin.site.register(User, DreamyUserAdmin)
admin.site.register(UserFollower)
admin.site.register(Post)
