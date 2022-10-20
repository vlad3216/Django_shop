from django.contrib.auth import urls
from django.urls import path, include

from users.views import registration

urlpatterns = [
    path('', include(urls)),
    path('registration/', registration, name='registration'),
]