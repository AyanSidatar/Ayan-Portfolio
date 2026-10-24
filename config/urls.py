from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from contact.views import contact
from content.views import home

urlpatterns = [
    path("", home, name="home"),
    path("contact/", contact, name="contact"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
