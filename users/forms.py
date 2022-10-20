from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

    def clean(self):
        self.instance.username = self.cleaned_data['email'].split('@')[0]
        try:
            User.objects.get(username=self.instance.username)
            raise ValidationError("A user with that username already exists.")
        except User.DoesNotExist:
            ...
        return self.cleaned_data