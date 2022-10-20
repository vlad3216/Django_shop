from django.shortcuts import render, redirect
from django.contrib.auth import login

from users.forms import RegistrationForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.save())
            return redirect('products')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'registration/registration.html', context)