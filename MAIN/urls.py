from django.urls import path

from MAIN.views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
]