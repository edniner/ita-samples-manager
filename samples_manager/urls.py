from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<experiment_id>[0-9]+)/experiment/$', views.experiment_details, name='experiment_details'),
    url(r'^logged_user/$', views.view_user, name='view_user'),
    url(r'^experiments/$', views.experiments_list, name='experiments_list'),
    url(r'^user/(?P<pk>\d+)/experiments/$', views.admin_experiments_user_view, name='admin_experiments_user_view'),
    url(r'^admin/experiments/$', views.admin_experiments_list, name='admin_experiments_list'),
    url(r'^experiment/new/$', views.experiment_new, name='experiment_new'),
    url(r'^experiments/(?P<pk>\d+)/update/$', views.experiment_update, name='experiment_update'),
    url(r'^experiments/(?P<pk>\d+)/delete/$', views.experiment_delete, name='experiment_delete'),
    url(r'^experiments/(?P<pk>\d+)/clone/$', views.experiment_clone, name='experiment_clone'),
    url(r'^experiments/(?P<pk>\d+)/validate/$', views.experiment_validate, name='experiment_validate'),
    url(r'^experiments/(?P<pk>\d+)/status/$', views.experiment_status_update, name='experiment_status_update'),
    url(r'^experiments/(?P<pk>\d+)/print/$', views.print_experiment_view, name='print_experiment_view'),
    url(r'^users/$', views.users_list, name='users_list'),
    url(r'^experiment/(?P<experiment_id>\d+)/users/$', views.experiment_users_list, name='experiment_users_list'),
    url(r'^experiment/(?P<experiment_id>\d+)/user/new/$', views.user_new, name='user_new'),
    url(r'^user/new/$', views.admin_user_new, name='admin_user_new'),
    url(r'^experiment/(?P<experiment_id>\d+)/user/(?P<pk>\d+)/update/$', views.user_update, name='user_update'),
    url(r'^experiment/(?P<experiment_id>\d+)/user/(?P<pk>\d+)/delete/$', views.user_delete_from_experiment, name='user_delete_from_experiment'),
    url(r'^user/(?P<pk>\d+)/delete/$', views.admin_user_delete, name='admin_user_delete'),
    url(r'^regulations/$',views.regulations, name='regulations'),
    url(r'^fluence_conversion/$',views.fluence_conversion, name='fluence_conversion'),
    url(r'^experiment/(?P<experiment_id>\d+)/samples/$', views.experiment_samples_list, name='experiment_samples_list'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/new/$', views.sample_new, name='sample_new'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/(?P<pk>\d+)/update/$', views.sample_update, name='sample_update'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/(?P<pk>\d+)/clone/$', views.sample_clone, name='sample_clone'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/(?P<pk>\d+)/delete/$', views.sample_delete, name='sample_delete'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/(?P<pk>\d+)/print/label/$', views.print_sample_label_view, name='print_sample_label_view'),
    url(r'^experiment/(?P<experiment_id>\d+)/sample/(?P<pk>\d+)/print/$', views.print_sample_view, name='print_sample_view'),
    url(r'^dosimeters/$', views.dosimeters_list, name='dosimeters_list'),
    url(r'^dosimeter/new/$', views.dosimeter_new, name='dosimeter_new'),
    url(r'^dosimeter/(?P<pk>\d+)/update/$', views.dosimeter_update, name='dosimeter_update'),
    url(r'^dosimeter/(?P<pk>\d+)/clone/$', views.dosimeter_clone, name='dosimeter_clone'),
    url(r'^dosimeter/(?P<pk>\d+)/delete/$', views.dosimeter_delete, name='dosimeter_delete'),
    url(r'^dosimeter/(?P<pk>\d+)/print/label/$', views.print_dosimeter_label_view, name='print_dosimeter_label_view'),
    url(r'^experiment/(?P<experiment_id>\d+)/dosimeter/assign/$', views.assign_dosimeters, name='assign_dosimeters'),
    url(r'^assign/samples/dosimeters/$', views.assign_samples_dosimeters, name='assign_samples_dosimeters'),
    url(r'^dosimeters/generate/ids/$', views.generate_dos_ids, name='generate_dos_ids'),
    url(r'^user/(?P<pk>\d+)/update/$', views.admin_user_update, name='admin_user_update'),
    url(r'^irradiations/$', views.irradiations, name='irradiations'),
    url(r'^search_irradiations/$', views.search_irradiations, name='search_irradiations'),
    url(r'^search/experiment/(?P<experiment_id>\d+)$', views.search_samples, name='search_samples'),
    url(r'^search/experiments/user$', views.search_experiments_user, name='search_experiments_user'),
    url(r'^search/admin/experiments/$', views.search_experiments_admin, name='search_experiments_admin'),
    url(r'^search/experiment/(?P<experiment_id>\d+)/users/$', views.search_experiment_users, name='search_experiment_users'),
    url(r'^search/admin/users/$', views.search_users_admin, name='search_users_admin'),
    url(r'^search/dosimeters/$', views.search_dosimeters, name='search_dosimeters'),
    url(r'^compound/new/$', views.compound_new, name='compound_new'),
    ]
