from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
<<<<<<< HEAD

urlpatterns = [
    path('', admin.site.urls),
=======


urlpatterns = [
    path('admin/', admin.site.urls),
>>>>>>> 0d3d1ea66e2c705bac8263807d4e1d17085d9a60

    path('api/v1/', include('authentication.urls')),
    path('api/v1/', include('decryptor.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
