from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView


admin.site.site_header = 'Learn SQL'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="users/main.html")),
    url(r'^console/', TemplateView.as_view(template_name="users/console.html")),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
]
