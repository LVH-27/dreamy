from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, ModelChoiceField, DateTimeField, HiddenInput
from .models import Post


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


class DreamySubmitPostForm(ModelForm):
    """This class defines the form to submit images to Dreamy"""

    author = ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput())
    date = DateTimeField(widget=HiddenInput())

    class Meta:
        """This class maps the form to the Post model definition"""

        model = Post
        fields = ['description', 'image']
