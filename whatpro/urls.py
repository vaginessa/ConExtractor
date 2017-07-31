from django.conf.urls import url
from django.contrib import admin
from whatsapp.views import Index, newsletter

urlpatterns = [
    url(r'^secretplace/', admin.site.urls),
    url(r'^newsletter-subscribe', newsletter),
    url(r'^$', Index.as_view()),
]
