from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from products.urls import urlpatterns as products_urlpatterns
from users.urls import urlpatterns as users_urlpatterns
from main.urls import urlpatterns as main_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(products_urlpatterns)),
    path('feedbacks/', include('feedbacks.urls')),
    path('', include(users_urlpatterns)),
    path('', include(main_urlpatterns)),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)