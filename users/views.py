from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_backends, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as AuthLoginView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, RedirectView
from django.conf import settings

from users.forms import ConfirmCodeForm, RegistrationForm,\
     CustomAuthenticationForm


User = get_user_model()

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            login(
                request,
                form.get_user(),
                'django.contrib.auth.backends.ModelBackend')
            return redirect('main')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'registration/registration.html', context)


class LoginView(AuthLoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        messages.success(self.request,
                         f'Welcome back {form.get_user().email}!')
        return super().form_valid(form)


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        if form.cleaned_data.get('phone'):
            self.success_url = reverse_lazy('confirmation_code')
            self.request.session['user_id'] = str(user.id)
        messages.success(self.request,
                         'Registration success!')
        return super().form_valid(form)


class RegistrationConfirmView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user = self.get_user(kwargs['uidb64'])

        if user is not None:
            token = kwargs['token']
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save(update_fields=('is_active',))
                messages.success(
                    request,
                    'Activation success. '
                    'You can login using your email and password.'
                )
            else:
                messages.error(request, 'Activation error.')
        return super().get(request, *args, **kwargs)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist,
                ValidationError):
            user = None
        return user


def confirm_code(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        form = ConfirmCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if code == cache.get(f'{str(user.id)}_code'):
                user.is_active = True
                user.is_phone_valid = True
                user.save(update_fields=('is_active', 'is_phone_valid'))
                return redirect('login')
            else:
                messages.error(request, 'Code not valid. Try again.')
    else:
        form = ConfirmCodeForm()
    return render(request, 'registration/confirmation.html', {'form': form})