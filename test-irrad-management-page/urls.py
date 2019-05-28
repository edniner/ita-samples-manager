from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    # Examples:
    # url(r'^$', 'test2_samples_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^samples_manager/', include('samples_manager.urls', namespace="samples_manager")),
    url(r'^admin/', include(admin.site.urls)),
]
