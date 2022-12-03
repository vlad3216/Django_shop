from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_backends
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.conf import settings

from users.forms import RegistrationForm, CustomAuthenticationForm


# def registration(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             login(
#                 request,
#                 form.get_user(),
#                 'django.contrib.auth.backends.ModelBackend')
#             return redirect('main')
#     else:
#         form = RegistrationForm()
#     context = {'form': form}
#     return render(request, 'registration/registration.html', context)


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
        backend = settings.AUTHENTICATION_BACKENDS[0]
        login(self.request, form.save(), backend)
        messages.success(self.request,
                         'Registration success!')
        return super().form_valid(form)