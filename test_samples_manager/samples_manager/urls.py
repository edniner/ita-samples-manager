from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<experiment_id>[0-9]+)/experiment/$', views.experiment_details, name='experiment_details'),
    url(r'^(?P<sample_id>[0-9]+)/sample/$', views.sample_details, name='sample_details'),
    url(r'^experiment/new/$', views.experiment_new, name='experiment_new'),
    url(r'^sample/new/$', views.sample_new, name='sample_new'),
    url(r'^user/new/$', views.user_new, name='user_new'),
    url(r'thankyou/$', views.thankyou, name='thankyou'),
]