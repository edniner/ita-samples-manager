from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<experiment_id>[0-9]+)/experiment/$', views.experiment_details, name='experiment_details'),
    url(r'^logged_user/$', views.view_user, name='view_user'),
    url(r'^experiments/$', views.experiments_list, name='experiments_list'),
    url(r'^experiments/all/$', views.all_experiments_list, name='all_experiments_list'),
    url(r'^admin/experiments/$', views.admin_experiments_list, name='admin_experiments_list'),
    url(r'^experiment/new/$', views.experiment_new, name='experiment_new'),
    url(r'^experiments/(?P<pk>\d+)/update/$', views.experiment_update, name='experiment_update'),
    url(r'^experiments/(?P<pk>\d+)/delete/$', views.experiment_delete, name='experiment_delete'),
    url(r'^experiments/(?P<pk>\d+)/clone/$', views.experiment_clone, name='experiment_clone'),
    url(r'^experiments/(?P<pk>\d+)/validate/$', views.experiment_validate, name='experiment_validate'),
    url(r'^experiments/(?P<pk>\d+)/print/$', views.print_experiment_view, name='print_experiment_view'),
    url(r'^users/$', views.users_list, name='users_list'),
    url(r'^experiment/(?P<experiment_id>\d+)/users/$', views.experiment_users_list, name='experiment_users_list'),
    url(r'^experiment/(?P<experiment_id>\d+)/user/new/$', views.user_new, name='user_new'),
    #url(r'^user/new/$', views.user_new, name='user_new'),
    url(r'^experiment/(?P<experiment_id>\d+)/user/(?P<pk>\d+)/update/$', views.user_update, name='user_update'),
    url(r'^experiment/(?P<experiment_id>\d+)/user/(?P<pk>\d+)/delete/$', views.user_delete, name='user_delete'),
    url(r'^regulations/$',views.regulations, name='regulations'),
    url(r'^fluence_conversion/$',views.fluence_conversion, name='fluence_conversion'),
    url(r'^experiment/(?P<experiment_id>\d+)/samples/$', views.experiment_samples_list, name='experiment_samples_list'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/new/$', views.sample_new, name='sample_new'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/(?P<pk>\d+)/update/$', views.sample_update, name='sample_update'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/(?P<pk>\d+)/clone/$', views.sample_clone, name='sample_clone'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/(?P<pk>\d+)/delete/$', views.sample_delete, name='sample_delete'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/(?P<pk>\d+)/print/$', views.print_sample_view, name='print_sample_view'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/(?P<pk>\d+)/print/label/$', views.print_sample_label_view, name='print_sample_label_view'),
    ]

