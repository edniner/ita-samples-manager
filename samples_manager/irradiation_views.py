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


def irradiations(request):
     tables = ['IRRAD1','IRRAD3','IRRAD5','IRRAD7','IRRAD9','IRRAD11','IRRAD13','IRRAD15','IRRAD17','IRRAD19']
     logged_user = get_logged_user(request)
     irradiations = Irradiation.objects.filter(~Q(status = 'Completed'))
     return render(request, 'samples_manager/irradiations_list.html', {'irradiations': irradiations,'tables': tables, 'logged_user': logged_user,})


def irradiation_status_update(request, pk):
    data = dict()
    logged_user = get_logged_user(request)
    irradiation = get_object_or_404(Irradiation, pk=pk)
    if request.method == 'POST':
        form =  IrradiationStatus(request.POST,instance=irradiation)
        if form.is_valid():
            updated_irradiation =  form.save()
            data['form_is_valid'] = True
            irradiations = Irradiation.objects.filter(~Q(status = 'Completed'))
            template_data = {'irradiations': irradiations, 'logged_user':logged_user, 'sec': '0','start_timestamp':'' }
            output_template = 'samples_manager/partial_irradiations_list.html'
            data['html_irradiation_list'] = render_to_string(output_template, template_data)
        else:
            print("form is not valid")
    else:
        form = IrradiationStatus(instance=irradiation)
    context = {'form': form, 'irradiation': irradiation}
    data['html_form'] = render_to_string('samples_manager/irradiation_status_update.html',
        context,
        request=request,
    )
    return JsonResponse(data)

def irradiation_new(request):
    data = dict()
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        form = IrradiationForm(request.POST)
        if form.is_valid():
            irradiation = Irradiation(in_beam = False, dos_position = form.cleaned_data['dos_position'])
            irradiation.save()
            irradiation.sample = form.cleaned_data['sample']
            irradiation.dosimeter = form.cleaned_data['dosimeter']
            irradiation.irrad_table = form.cleaned_data['irrad_table']
            irradiation.table_position = form.cleaned_data['table_position']
            irradiation.sec = form.cleaned_data['sec']
            irradiation.accumulated_fluence = form.cleaned_data['accumulated_fluence']
            irradiation.fluence_error = form.cleaned_data['fluence_error']
            irradiation.date_in = form.cleaned_data['date_in']
            irradiation.date_out = form.cleaned_data['date_out']
            irradiation.comments = form.cleaned_data['comments']
            irradiation.status = "Registered"
            irradiation.updated_by = logged_user
            irradiation.save()
            irradiations = Irradiation.objects.filter(~Q(status = 'Completed'))
            data['form_is_valid'] = True
            data['html_irradiation_list'] = render_to_string('samples_manager/partial_irradiations_list.html',{'irradiations': irradiations, 'logged_user': logged_user, 'sec':'0', 'start_timestamp': ''})
        else:
            data['form_is_valid'] = False
    else:
        form = IrradiationForm()
        context = {'form': form, 'logged_user': logged_user}
        data['html_form'] = render_to_string('samples_manager/partial_irradiation_form.html',
                    context,
                    request=request,
                )
    return JsonResponse(data)

def irradiation_update(request, pk):
    data = dict()
    logged_user = get_logged_user(request)
    irradiation = get_object_or_404(Irradiation, pk=pk)
    if request.method == 'POST':
        form = IrradiationForm(request.POST, instance = irradiation)
        if form.is_valid():
            form.save()
            irradiations = Irradiation.objects.filter(~Q(status = 'Completed'))
            data['form_is_valid'] = True
            data['html_irradiation_list'] = render_to_string('samples_manager/partial_irradiations_list.html',{'irradiations': irradiations, 'logged_user': logged_user, 'sec': '0','start_timestamp':''})
        else:
            data['form_is_valid'] = False
    else:
        form = IrradiationForm(instance = irradiation)
        context = {'form': form, 'logged_user': logged_user}
        data['html_form'] = render_to_string('samples_manager/partial_irradiation_form_update.html',
                    context,
                    request=request,
                )
    return JsonResponse(data)

def irradiation_delete(request ,pk):
    print("irradiation_delete")
    irradiation = get_object_or_404(Irradiation, pk=pk)
    logged_user = get_logged_user(request)
    data = dict()
    if request.method == 'POST':
        irradiation.delete()
        data['form_is_valid'] = True 
        irradiations = Irradiation.objects.filter(~Q(status = 'Completed'))
        data['html_irradiation_list'] = render_to_string('samples_manager/partial_irradiations_list.html',{'irradiations': irradiations, 'logged_user': logged_user, 'sec': '0', 'start_timestamp':''},request=request,)
    else:
        context = {'irradiation': irradiation,}
        data['html_form'] = render_to_string('samples_manager/partial_irradiation_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)


def new_group_irradiation(request, experiment_id):
    data = dict()
    #print("new_irradiation")
    selected_samples = []
    if request.method == 'POST':
        checked_samples = request.POST.getlist('checks[]')
        for sample in checked_samples:
                    sample_splitted = sample.split("<")
                    sample_name = sample_splitted[6].split(">")[1]
                    sample_object = Samples.objects.get(name = sample_name)
                    selected_samples.append(sample_object.name)
    data['request_valid'] = True
    form = GroupIrradiationForm()
    request.session['selected_samples'] = selected_samples
    context = {'form': form, 'experiment_id': experiment_id,'selected_samples':selected_samples}    
    #print("before rendering")
    data['html_form'] = render_to_string('samples_manager/partial_group_irradiation_form.html', context, request=request)
    #print("selected:",selected_samples)
    return JsonResponse(data)


def admin_dosimetry_results(request):
    logged_user = get_logged_user(request)
    results = Irradiation.objects.all()
    return render(request, 'samples_manager/admin_dosimetry_results.html', {'results': results, 'logged_user':logged_user})

def dosimetry_results(request, sample_id):
    logged_user = get_logged_user(request)
    results = Irradiation.objects.filter(sample = sample_id)
    sample = get_object_or_404(Samples, pk=sample_id)
    sample_fluences = get_sample_fluences(sample)
    return render(request, 'samples_manager/dosimetry_results.html', {'sample':sample, 'results': results, 'logged_user':logged_user,'sample_fluences':sample_fluences})
