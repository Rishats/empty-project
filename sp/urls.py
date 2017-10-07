from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="users/main.html")),
    url(r'^console/', TemplateView.as_view(template_name="users/console.html")),
]
