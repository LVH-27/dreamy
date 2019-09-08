from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


User = get_user_model()


class DreamyUserCreationForm(UserCreationForm):
    """
    This class overrides the default UserCreation form to use the
    overridden User model definition
    """

    class Meta(UserCreationForm.Meta):
        """This class overrides the User model definition"""

        model = User
        fields = ['username', 'bio', 'avatar']


class DreamyUserChangeForm(UserChangeForm):
    """
    This class overrides the default UserCreation form to use the
    overridden User model definition
    """

    class Meta(UserChangeForm.Meta):
        """This class overrides the User model definition"""

        model = User
