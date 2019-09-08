from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


User = get_user_model()


class DreamyUserCreationForm(UserCreationForm):
    """
    This class overrides the default UserCreation form to use the
    overridden User model definition
    """

    class Meta(UserCreationForm):
        """This class overrides the User model definition"""

        model = User
        fields = ['username', 'password', 'bio']

    def __init__(self, *args, **kwargs):
        """Override the constructor to set select fields to not required."""
        super(DreamyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['bio'].required = False
        # self.fields['birth_date'].required = False
        # self.fields['avatar'].required = False


class DreamyUserChangeForm(UserChangeForm):
    """
    This class overrides the default UserCreation form to use the
    overridden User model definition
    """

    class Meta(UserChangeForm):
        """This class overrides the User model definition"""

        model = User
        fields = ['username', 'password', 'bio']

    def __init__(self, *args, **kwargs):
        """Override the constructor to set select fields to not required."""
        super(DreamyUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['bio'].required = False
        # self.fields['birth_date'].required = False
        # self.fields['avatar'].required = False
