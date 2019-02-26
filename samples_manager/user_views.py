from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import *
from django.template import loader
from django.core.urlresolvers import reverse
import datetime
from .forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from io import BytesIO
from django.utils.safestring import mark_safe
import logging 
from django.db.models import Q
from django.utils import timezone
from django.db import connection
import re
from datetime import date
import random
import time
from django.utils.datastructures import MultiValueDictKeyError
from .views import *

def save_user_form(request, form, experiment, template_name):
    data = dict()
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        if form.is_valid():
            users = Users.objects.all()
            emails = []
            for item in users:
                emails.append(item.email)
            if form.cleaned_data is not None:
                submited_user = form.cleaned_data
                if  not submited_user["email"] in emails:
                    user = form.save()
                    email = user.email 
                    user.email = email.lower()
                    user.save()
                    experiment.users.add(user)
                else:
                    user = Users.objects.get( email = submited_user["email"])
                    user.name =  submited_user["name"]
                    user.surname =  submited_user["surname"]
                    user.telephone =  submited_user["telephone"]
                    user.role =  submited_user["role"]
                    user.save()
                    if submited_user["email"] !=  experiment.responsible.email:
                        experiment.users.add(user)
                message=mark_safe('Dear user,\nyou were assigned as a user for the experiment '+experiment.title+' by the account: '+logged_user.email+'.\nPlease, find all your experiments at this URL: http://cern.ch/irrad.data.manager/samples_manager/experiments/\nIn case you believe that this e-mail has been sent to you by mistake please contact us at irrad.ps@cern.ch.\nKind regards,\nCERN IRRAD team.\nhttps://ps-irrad.web.cern.ch')
                send_mail_notification('IRRAD Data Manager: Registration to the experiment %s of CERN IRRAD Proton Irradiation Facility' %experiment.title,message,'irrad.ps@cern.ch', user.email)
            data['form_is_valid'] = True
            users = experiment.users.all()
            data['html_user_list'] = render_to_string('samples_manager/partial_users_list.html', {
                'users': users,
                'experiment':experiment
            })
            data['state'] = "Created"
            print(data)
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'experiment': experiment}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def view_user(request):
    #only in production
    logged_user = get_logged_user(request)
    #logged_user = 'blerina.gkotse@cern.ch'
    html = "<html><body><div id='user_id'>User e-mail %s.</div></body></html>" %  logged_user.email
    return HttpResponse(html)

def users_list(request):
    logged_user = get_logged_user(request)
    preference = define_preferences(request)
    users = Users.objects.all()
    users_data = []
    row = 0
    for user in users: 
        row = row + 1 
        experiment_values = Experiments.objects.filter(Q(users=user)|Q(responsible=user)).values('title').distinct()
        experiment_number = 0
        if experiment_values:
            experiments_number = experiment_values.count()
        else:
            experiments_number = 0
        users_data.append({
            "user":user,
            "experiments_number":experiments_number,
            "row": row
        })
    return render(request, 'samples_manager/admin_users_list.html', {'users_data': users_data,'logged_user': logged_user, 'prefered_theme':preference['global_theme'], 'prefered_button':preference['button_theme'],'prefered_menu':preference['menu_theme'],'prefered_table':preference['table_theme']})


def admin_user_new(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
    else:
        form = UsersForm()
    return save_admin_user_form(request, form, 'samples_manager/admin_partial_user_create.html')

def save_admin_user_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            users = Users.objects.all()
            users_data = []
            row = 0 
            for user in users: 
                row = row + 1 
                experiment_values = Experiments.objects.filter(Q(users=user)|Q(responsible=user)).values('title').distinct()
                experiment_number = 0
                if experiment_values:
                    experiments_number = experiment_values.count()
                else:
                    experiments_number = 0
                users_data.append({
                    "user":user,
                    "experiments_number":experiments_number,
                    "row": row,
                })
            data['html_user_list'] = render_to_string('samples_manager/admin_partial_users_list.html', {
                'users_data': users_data,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def experiment_users_list(request, experiment_id):
    print("experiment users list")
    preference = define_preferences(request)
    experiment = Experiments.objects.get(pk = experiment_id)
    logged_user = get_logged_user(request)
    if (logged_user.email != experiment.responsible.email) and (logged_user not in experiment.users.all()) and logged_user.role != 'Admin':
        return render(request,'samples_manager/not_allowed_user.html',{'logged_user': logged_user})
    else:
        users= experiment.users.values()
        return render(request, 'samples_manager/users_list.html', {'users': users,'experiment': experiment,'logged_user': logged_user, 'prefered_theme':preference['global_theme'],'prefered_button':preference['button_theme'],'prefered_menu':preference['menu_theme'],'prefered_table':preference['table_theme'] })

def user_new(request,experiment_id):
    experiment = Experiments.objects.get(pk = experiment_id)
    if request.method == 'POST':
        form = UsersForm(request.POST)
    else:
        form = UsersForm()
    return save_user_form(request, form,experiment, 'samples_manager/partial_user_create.html')

def user_update(request,experiment_id,pk):
    experiment = Experiments.objects.get(pk = experiment_id)
    user = get_object_or_404(Users, pk=pk)
    if request.method == 'POST':
        form = UsersForm(request.POST, instance=user)
    else:
        form = UsersForm(instance=user)
    return save_user_form(request, form, experiment,'samples_manager/partial_user_update.html')

def user_delete_from_experiment(request,experiment_id,pk):
    experiment = Experiments.objects.get(pk = experiment_id)
    user = get_object_or_404(Users, pk=pk)
    data = dict()
    if request.method == 'POST':
        #user.delete()
        experiment.users.remove(user)
        data['form_is_valid'] = True  
        users = experiment.users.all()
        data['html_user_list'] = render_to_string('samples_manager/partial_users_list.html', {
            'users': users,
            'experiment':experiment
        })
        data['state'] = "Deleted"
    else:
        context = {'user': user, 'experiment':experiment,}
        data['html_form'] = render_to_string('samples_manager/partial_user_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def admin_user_delete(request ,pk):
    user = get_object_or_404(Users, pk=pk)
    data = dict()
    if request.method == 'POST':
        user.delete()
        data['form_is_valid'] = True 
        users = Users.objects.all()
        row = 0 
        for user in users:
            row = row + 1 
            experiment_values = Experiments.objects.filter(Q(users=user)|Q(responsible=user)).values('title').distinct()
            experiment_number = 0
            if experiment_values:
                experiments_number = experiment_values.count()
            else:
                experiments_number = 0
            users_data.append({
                "user":user,
                "experiments_number":experiments_number,
                "row": row,
            })
        data['html_user_list'] = render_to_string('samples_manager/admin_partial_users_list.html', {
            'users_data': users_data,
            'logged_user': logged_user
        })
        data['state'] = "Deleted"
    else:
        context = {'user': user,}
        data['html_form'] = render_to_string('samples_manager/admin_partial_user_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
    
def admin_user_update(request,pk):
    user = get_object_or_404(Users, pk = pk)
    if request.method == 'POST':
        form = UsersForm(request.POST, instance = user)
    else:
        form = UsersForm(instance = user)
    return save_admin_user_form(request, form,'samples_manager/admin_partial_user_update.html')

#!!! to be continued
def users_samples(request):
    logged_user = get_logged_user(request)
    samples = authorised_samples(logged_user)
    return render(request, 'samples_manager/samples_list.html', {'samples': samples,'logged_user': logged_user})
    
