from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('intersecter.urls'))
]

# Jeśli zobaczy w przeglądarce adres zaczynający się od /media/ (MEDIA_URL),
# to nie szuka widoku w views.py, tylko prosto do folderu na dysku zdefiniowanego jako
# MEDIA_ROOT. Te dwie linijki zapewniają że django umie znaleźć postery filmów
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
