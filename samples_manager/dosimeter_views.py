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

def dosimeters_list(request):
    logged_user = get_logged_user(request)
    dosimeters = Dosimeters.objects.order_by('dos_id')
    return render(request, 'samples_manager/dosimeters_list.html', {'dosimeters': dosimeters, 'logged_user': logged_user,})

def dosimeter_new(request):
    logged_user = get_logged_user(request)
    print("dosimeter new")
    if request.method == 'POST':
        form1 = DosimetersForm1(request.POST)
        form2 = DosimetersForm2(request.POST)
    else:
        form1 = DosimetersForm1()
        form2 = DosimetersForm2(initial={'responsible': logged_user })
    status = 'new'
    return save_dosimeter_form(request, form1, form2,status, 'samples_manager/partial_dosimeter_create.html')

def dosimeter_update(request, pk):
    dosimeter = get_object_or_404(Dosimeters, pk=pk)
    if request.method == 'POST':
        form1 = DosimetersForm1(request.POST, instance=dosimeter)
        form2 = DosimetersForm2(request.POST, instance=dosimeter)
    else:
        form1 = DosimetersForm1(instance=dosimeter)
        form2 = DosimetersForm2(instance=dosimeter)
    status = 'update'
    print("dosimeter_update")
    return save_dosimeter_form(request, form1, form2, status,'samples_manager/partial_dosimeter_update.html')

def dosimeter_clone(request, pk):
    dosimeter = get_object_or_404(Dosimeters, pk=pk)
    if request.method == 'POST':
        form1 = DosimetersForm1(request.POST)
        form2 = DosimetersForm2(request.POST)
    else:
        form1 = DosimetersForm1(instance=dosimeter, initial={'dos_id': ''})
        form2 = DosimetersForm2(instance=dosimeter)
    status = 'clone'
    return save_dosimeter_form(request,  form1, form2, status,'samples_manager/partial_dosimeter_create.html')

def dosimeter_delete(request, pk):
    dosimeter = get_object_or_404(Dosimeters, pk=pk)
    data = dict()
    if request.method == 'POST':
        dosimeter.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        dosimeters = Dosimeters.objects.order_by('dos_id')
        data['html_dosimeter_list'] = render_to_string('samples_manager/partial_dosimeters_list.html', {
            'dosimeters': dosimeters
        })
    else:
        context = {'dosimeter': dosimeter}
        data['html_form'] = render_to_string('samples_manager/partial_dosimeter_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def generate_dos_id(dosimeter):
    if dosimeter.dos_id =='':
        all_dosimeters = Dosimeters.objects.all()
        dosimeters_numbers = []
        for dosimeter in all_dosimeters:
            if dosimeter.dos_id !='': 
                 dosimeters_numbers.append(int(dosimeter.dos_id[4:10]))
            else:
                dosimeters_numbers.append(0)  
        dosimeters_numbers.sort(reverse=False)
        assigned_dosimeters = []
        for dosimeter in dosimeters_numbers: 
            if 3999<dosimeter:
                assigned_dosimeters.append(dosimeter)
        available_dos_id = 0
        for (idx,val) in enumerate(assigned_dosimeters):
            if idx == 0:
                pass
            else:
                if val==assigned_dosimeters[idx-1]+1 or val==assigned_dosimeters[idx-1]:
                    pass 
                else:
                    available_dos_id = assigned_dosimeters[idx-1]+1
                    break
        if available_dos_id == 0:
            dosimeters_numbers.sort(reverse=True)
            if 3999<dosimeters_numbers[0]:
                new_dosimeter_dos_id_number_int = dosimeters_numbers[0] + 1
            else:
                new_dosimeter_dos_id_number_int = 4000
        else:
            new_dosimeter_dos_id_number_int = available_dos_id
        new_dosimeter_dos_id_number = "" + str(new_dosimeter_dos_id_number_int)
        zeros = 6-len(new_dosimeter_dos_id_number)
        for x in range(0,zeros):
            new_dosimeter_dos_id_number = "0"+ new_dosimeter_dos_id_number
        new_dosimeter_dos_id = "DOS-"+ new_dosimeter_dos_id_number
        return new_dosimeter_dos_id
    else:
        return dosimeter.dos_id

def generate_dos_ids(request):
    data = dict()
    if request.method == 'POST':
        number_ids = int(request.POST['number_ids'])
        for i in range(0,number_ids):
            dosimeter = Dosimeters(status = "Registered", dos_type = "Aluminium")
            dosimeter.save()
            dosimeter.dos_id = generate_dos_id(dosimeter)
            dosimeter.save()
        data['form_is_valid'] = True
        dosimeters = Dosimeters.objects.order_by('dos_id')
        data['html_dosimeter_list'] = render_to_string('samples_manager/partial_dosimeters_list.html', {
                'dosimeters':dosimeters
            })
    context = {}
    data['html_form'] = render_to_string('samples_manager/generate_dos_ids.html',
        context,
        request=request,
        )
    return JsonResponse(data)

def assign_dosimeters(request, experiment_id):
    data = dict()
    sample_names = request.session['selected_samples']
    logged_user = get_logged_user(request)
    samples = []
    for sample_name in sample_names:
        sample = Samples.objects.get(name = sample_name)
        samples.append(sample)
    if request.method == 'POST':
        form = GroupIrradiationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data is not None:
                dosimeter = form.cleaned_data['dosimeter']
                for sample in samples: 
                        irradiation = Irradiation(in_beam = False, dos_position = 1)
                        irradiation.save()
                        irradiation.sample = sample
                        irradiation.dosimeter = dosimeter
                        irradiation.irrad_table = form.cleaned_data['irrad_table']
                        irradiation.table_position = form.cleaned_data['table_position']
                        irradiation.status = "Registered"
                        irradiation.updated_by = logged_user
                        irradiation.created_by = logged_user
                        irradiation.dos_position = 1
                        irradiation.save()
            irradiations = Irradiation.objects.filter(~Q(status = 'Completed'))
            data['form_is_valid'] = True
            data['html_irradiation_list'] = render_to_string('samples_manager/irradiations_list.html',{'irradiations': irradiations, 'logged_user': logged_user, 'sec': '0','start_timestamp':''})
        else:
            print(form)
            data['form_is_valid'] = False
    else:
        form = GroupIrradiationForm()
        context = {'form': form, 'experiment_id':  experiment_id, 'samples': samples}
        data['html_form'] = render_to_string('samples_manager/partial_group_irradiation_form.html',
                context,
                request=request,
            )
    return JsonResponse(data)

