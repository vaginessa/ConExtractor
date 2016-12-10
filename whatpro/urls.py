from django.conf.urls import url
from django.contrib import admin
from whatsapp.views import Index
from django.views import View

urlpatterns = [
    url(r'^secretplace/', admin.site.urls),
    url(r'^$', Index.as_view())
]
