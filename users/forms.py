import random
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,\
     UsernameField
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from shop1.helper import send_html_mail
from users.tasks import send_sms


User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             required=False)
    phone = forms.CharField(required=False)

    field_order = ['username', 'phone', 'password']

    def clean(self):
        username = self.cleaned_data.get('username')
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')

        if not username and not phone:
            raise ValidationError('Email or phone number is required.')

        if password:
            kwargs = {'password': password, 'username': username}
            if phone and not username:
                kwargs.pop('username')
                kwargs.update({'phone': phone})
            self.user_cache = authenticate(self.request, **kwargs)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2',)

    def clean(self):
        try:
            User.objects.get(email=self.instance.email)
            raise ValidationError("A user with that username already exists.")
        except User.DoesNotExist:
            ...
        self.instance.is_active = False
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        context = {
            'email': user.email,
            'domain': settings.DOMAIN,
            'site_name': 'SHOP',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'subject': 'Confirm registration'
        }
        subject_template_name = 'emails/registration/registration_confirm_subject.txt'  # noqa
        email_template_name = 'emails/registration/registration_confirm_email.html'  # noqa
        send_html_mail(
            subject_template_name,
            email_template_name,
            from_email=settings.SERVER_EMAIL,
            to_email=user.email,
            context=context
        )

        if self.cleaned_data.get('phone'):
            code = random.randint(10000, 99999)
            cache.set(f'{str(user.id)}_code', str(code), timeout=60)
            send_sms.delay(self.cleaned_data.get('phone'), code)
        return user


class ConfirmCodeForm(forms.Form):
    code = forms.CharField(max_length=5, required=True, help_text='Enter code')