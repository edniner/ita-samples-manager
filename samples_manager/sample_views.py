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

def save_sample_form(request,form1,form2,layers_formset, form3, status, experiment, template_name):
    data = dict()
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and layers_formset.is_valid():
            if status == 'new':
                if form1.checking_unique_sample() == True:
                    sample_data = {}
                    sample_data.update(form1.cleaned_data)
                    sample_data.update(form2.cleaned_data)
                    sample_data.update(form3.cleaned_data)
                    sample_temp = Samples.objects.create(**sample_data)
                    sample = Samples.objects.get(pk = sample_temp.pk)
                    sample.status = "Registered"
                    sample.created_by = logged_user
                    sample.updated_by = logged_user
                    sample.experiment = experiment
                    sample.save()
                    #print ("sample saved")
                    if layers_formset.is_valid():
                        #print("layers valid")
                        if  not layers_formset.cleaned_data:
                            print("layers missing")
                            data['state'] = 'layers missing'
                            data['form_is_valid'] = False
                        else: 
                            print("saving layers_formset")
                            for form in layers_formset.forms:
                                layer = form.save()
                                layer.sample = sample
                                print("layer sample save")
                                layer.save()   
                            data['state'] = "Created"
                            data['form_is_valid'] = True
                            save_occupancies(sample, status)
                            samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
                            samples_data = get_samples_occupancies(samples)
                            data['html_sample_list'] = render_to_string('samples_manager/partial_samples_list.html', {
                                'samples':samples,
                                'samples_data': samples_data,
                                'experiment': experiment
                            })
                else:
                    data['form_is_valid'] = False
                    data['state'] = "not unique"     
            elif status == 'update': 
                sample_temp = form1.save()
                form2.save()
                form3.save()
                sample_updated = Samples.objects.get(pk = sample_temp.pk)
                sample_updated.status = "Updated"
                sample_updated.updated_by = logged_user
                sample_updated.experiment = experiment
                sample_updated.save()
                if layers_formset.is_valid():
                    layers_formset.save()
                data['state'] = "Updated"
                data['form_is_valid'] = True
                save_occupancies(sample_updated, status)
                samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
                samples_data = get_samples_occupancies(samples)
                data['html_sample_list'] = render_to_string('samples_manager/partial_samples_list.html', {
                        'samples':samples,
                        'samples_data': samples_data,
                        'experiment': experiment
                })
            elif status == 'clone':
                print("clone")
                if form1.checking_unique_sample() == True:
                    sample_data = {}
                    sample_data.update(form1.cleaned_data)
                    sample_data.update(form2.cleaned_data)
                    sample_data.update(form3.cleaned_data)
                    sample_data.update({'status':'Registered', 'created_by':logged_user, 'updated_by': logged_user, 'experiment': experiment  })
                    sample = Samples.objects.create(**sample_data)
                    if layers_formset.is_valid():
                        if  not layers_formset.cleaned_data:
                            data['state'] = 'layers missing'
                            data['form_is_valid'] = False
                        else: 
                            for lay in layers_formset.cleaned_data:
                                    layer = Layers()
                                    layer.name = lay['name']
                                    print(layer.name)
                                    layer.length = lay['length']
                                    layer.compound_type = lay['compound_type']
                                    layer.sample = sample
                                    layer.save()
                            data['state'] = "Created"
                            data['form_is_valid'] = True
                            save_occupancies(sample, status)
                            samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
                            samples_data = get_samples_occupancies(samples)
                            data['html_sample_list'] = render_to_string('samples_manager/partial_samples_list.html', {
                                'samples':samples,
                                'samples_data': samples_data,
                                'experiment': experiment
                            })
                else:
                    data['form_is_valid'] = False
                    data['state'] = "not unique"   
            else:
                sample_updated = form1.save()
                form2.save()
                form3.save()
                sample_updated.save()
                if layers_formset.is_valid():
                    layers_formset.save()
                data['state'] = "Updated"
                data['form_is_valid'] = True
                save_occupancies(sample_updated, status)
                samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
                samples_data = get_samples_occupancies(samples)
                data['html_sample_list'] = render_to_string('samples_manager/partial_samples_list.html', {
                    'samples':samples,
                    'samples_data': samples_data,
                    'experiment': experiment
                })
        else:
            data['form_is_valid'] = False
            data['state'] = "missing fields"   
            logging.warning('Sample data invalid')
    context = {'form1': form1,'form2': form2,'form3': form3,'layers_formset': layers_formset,'experiment':experiment}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def archive_experiment_samples(request,experiment_id):
    logged_user = get_logged_user(request)
    experiment =  Experiments.objects.get(pk = experiment_id)
    archives = ArchiveExperimentSample.objects.filter(experiment = experiment)
    print(archives)
    return render(request, 'samples_manager/archive_experiment_samples.html', {'archives': archives, 'logged_user':logged_user, 'experiment': experiment})

def generate_set_id(sample):
    if sample.set_id =="":
        all_samples = Samples.objects.all()
        samples_numbers = []
        for sample in all_samples:
            if sample.set_id !="": 
                 samples_numbers.append(int(sample.set_id[4:]))
            else:
                samples_numbers.append(0)  
        samples_numbers.sort(reverse=False)
        assigned_samples = []
        for sample in samples_numbers: 
            if 3199<sample:
                assigned_samples.append(sample)
        available_set_id = 0
        for (idx,val) in enumerate(assigned_samples):
            if idx == 0:
                pass
            else:
                if val==assigned_samples[idx-1]+1:
                    pass 
                else:
                    available_set_id = assigned_samples[idx-1]+1
                    break
        if available_set_id == 0:
            samples_numbers.sort(reverse=True)
            if 3199<samples_numbers[0]:
                new_sample_set_id_number_int = samples_numbers[0] + 1
            else:
                new_sample_set_id_number_int = 3200
        else:
            new_sample_set_id_number_int = available_set_id
        new_sample_set_id_number = "" + str(new_sample_set_id_number_int)
        zeros = 6-len(new_sample_set_id_number)
        for x in range(0,zeros):
            new_sample_set_id_number = "0"+ new_sample_set_id_number
        new_sample_set_id = "SET-"+ new_sample_set_id_number
        return new_sample_set_id
    else:
        return sample.set_id

def assign_set_ids(request, experiment_id): 
    print("assigning set ids")
    experiment = Experiments.objects.get(pk = experiment_id)
    logged_user = get_logged_user(request)
    data = dict()
    if request.method == 'POST':
        data['form_is_valid'] = True
        checked_samples = request.POST.getlist('checks[]')
        for sample in checked_samples:
                    sample_splitted = sample.split("<")
                    if sample_splitted[0] == "":
                        sample_name = sample_splitted[6].split(">")[1]
                        sample_object = Samples.objects.get(name = sample_name)
                        sample_object.set_id = generate_set_id(sample_object)
                        sample_object.save()
                    else:
                        sample_object = Samples.objects.get(set_id = sample_splitted[0])
    samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
    samples_data = get_samples_occupancies(samples)
    context =  {'samples': samples, 'samples_data': samples_data, 'experiment': experiment,'logged_user': logged_user}
    if  logged_user.role == 'Admin': 
        data['html_sample_list'] =  render_to_string('samples_manager/partial_samples_list.html', context, request=request)
    else:
        data['html_sample_list'] =  render_to_string('samples_manager/partial_samples_list.html', context, request=request)
    return JsonResponse(data)


def experiment_samples_list(request, experiment_id):
    logged_user = get_logged_user(request)
    experiment = Experiments.objects.get(pk = experiment_id)
    if (logged_user.email != experiment.responsible.email) and (logged_user not in experiment.users.all()) and logged_user.role != 'Admin':
        return render(request,'samples_manager/not_allowed_user.html',{'logged_user': logged_user})
    else:
        samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
        samples_data = get_samples_occupancies(samples)
        experiments = authorised_experiments(logged_user)
        if  logged_user.role == 'Admin': 
            template_url = 'samples_manager/admin_samples_list.html'
        else: 
            template_url = 'samples_manager/samples_list.html'
        return render(request,template_url, {'samples': samples,'samples_data': samples_data, 'experiment': experiment,'logged_user': logged_user, 'experiments':experiments})

def admin_samples_list(request):
     template_url = 'samples_manager/samples_list.html'
     logged_user = get_logged_user(request)
     samples = Samples.objects.all()
     samples_data = get_samples_occupancies(samples)
     return render(request,template_url, {'samples': samples, 'logged_user': logged_user, 'samples_data': samples_data})


def search_samples(request, experiment_id):
        query_string = ''
        found_entries = None
        samples = []
        logged_user = get_logged_user(request)
        experiment = Experiments.objects.get(pk = experiment_id)
        samples_data = []
        if  logged_user.role == 'Admin': 
            template_url = 'samples_manager/admin_samples_list.html'
        else: 
            template_url = 'samples_manager/samples_list.html'
        if ('search_box' in request.GET) and request.GET['search_box'].strip():
            query_string = request.GET['search_box']
            entry_query = get_query(query_string, ['set_id', 'name', 'category','updated_by__email'])
            samples = Samples.objects.filter(entry_query, experiment = experiment)
            samples_data = get_samples_occupancies(samples)
        return render(request, template_url, {'samples': samples,'samples_data': samples_data, 'experiment': experiment,'logged_user': logged_user,})


def search_single_sample(request):
        query_string = ''
        found_entries = None
        samples = []
        logged_user = get_logged_user(request)
        samples_data = []
        if  logged_user.role == 'Admin': 
            template_url = 'samples_manager/admin_samples_list.html'
        else: 
            template_url = 'samples_manager/samples_list.html'
        if ('search_box' in request.GET) and request.GET['search_box'].strip():
            query_string = request.GET['search_box']
            entry_query = get_query(query_string, ['set_id', 'name', 'category','updated_by__email'])
            samples = Samples.objects.filter(entry_query)
            samples_data = get_samples_occupancies(samples)
        return render(request, template_url, {'samples': samples,'samples_data': samples_data,'logged_user': logged_user,})



def sample_new(request, experiment_id):
    experiment = Experiments.objects.get(pk = experiment_id)
    LayerFormset = inlineformset_factory( Samples, Layers, form = LayersForm, extra=0, min_num=1,validate_min=True, error_messages="Layers not correctly filled.", formset = LayersFormSet)
    if request.method == 'POST':
        form1 = SamplesForm1(request.POST, experiment_id = experiment.id)
        form2 = SamplesForm2(request.POST, experiment_id = experiment.id)
        layers_formset = LayerFormset(request.POST)
        form3 = SamplesForm3(request.POST, experiment_id = experiment.id)
    else:
        form1 = SamplesForm1(experiment_id = experiment.id)
        form2 = SamplesForm2(experiment_id = experiment.id)
        layers_formset = LayerFormset()
        form3 = SamplesForm3(experiment_id = experiment.id)
    status = 'new'
    return save_sample_form(request,form1,form2,layers_formset,form3,status,experiment,'samples_manager/partial_sample_create.html')


def sample_update(request, experiment_id, pk):
    experiment = Experiments.objects.get(pk = experiment_id)
    sample = get_object_or_404(Samples, pk=pk)
    LayersFormset = inlineformset_factory(Samples, Layers,form=LayersForm,extra=1)
    if request.method == 'POST':
        form1 = SamplesForm1(request.POST, instance=sample, experiment_id = experiment.id)
        form2 = SamplesForm2(request.POST, instance=sample, experiment_id = experiment.id)
        form3 = SamplesForm3(request.POST, instance=sample, experiment_id = experiment.id)
        layers_formset = LayersFormset(request.POST, instance=sample)
    else:
        form1 = SamplesForm1(instance=sample, experiment_id = experiment.id)
        form2 = SamplesForm2(instance=sample, experiment_id = experiment.id)
        form3 = SamplesForm3(instance=sample, experiment_id = experiment.id)
        layers_formset = LayersFormset(instance=sample)
    status = 'update'
    return save_sample_form(request, form1,form2,layers_formset, form3, status,experiment, 'samples_manager/partial_sample_update.html')

def sample_clone(request, experiment_id, pk):
    experiment = Experiments.objects.get(pk = experiment_id)
    sample = get_object_or_404(Samples, pk=pk)
    LayersFormset = inlineformset_factory(Samples,Layers,form=LayersForm,extra=0)
    if request.method == 'POST':
        form1 = SamplesForm1(request.POST, experiment_id = experiment.id, instance=sample)
        form2 = SamplesForm2(request.POST, experiment_id = experiment.id, instance=sample)
        form3 = SamplesForm3(request.POST, experiment_id = experiment.id, instance=sample)
        layers_formset = LayersFormset(request.POST,instance=sample)
    else:
        form1 = SamplesForm1(experiment_id = experiment.id, instance=sample, initial={'set_id': ""})
        form2 = SamplesForm2(experiment_id = experiment.id, instance=sample)
        form3 = SamplesForm3(experiment_id = experiment.id, instance=sample)
        layers_formset = LayersFormset(instance=sample)
    status = 'clone'
    return save_sample_form(request, form1,form2,layers_formset, form3, status, experiment, 'samples_manager/partial_sample_clone.html')

def sample_delete(request,experiment_id, pk):
    experiment = Experiments.objects.get(pk = experiment_id)
    sample = get_object_or_404(Samples, pk=pk)
    data = dict()
    if request.method == 'POST':
        sample.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
        samples_data = get_samples_occupancies(samples)
        data['html_sample_list'] = render_to_string('samples_manager/partial_samples_list.html', {
            'samples': samples,
            'samples_data': samples_data,
            'experiment': experiment
        })
    else:
        context = {'sample': sample, 'experiment': experiment }
        data['html_form'] = render_to_string('samples_manager/partial_sample_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)


def move_samples(request, experiment_id):
    #print("move samples")
    data = dict()
    logged_user = get_logged_user(request)
    experiment = Experiments.objects.get(pk = experiment_id)
    experiments = authorised_experiments(logged_user)
    if request.method == 'POST':
        checked_samples = request.POST.getlist('checks[]')
        new_experiment_value = request.POST.get("new_experiment","")
        new_experiment = Experiments.objects.get(pk = new_experiment_value)
        for sample in checked_samples:
                    sample_splitted = sample.split("<")
                    sample_name = sample_splitted[6].split(">")[1]
                    sample_object = Samples.objects.get(name = sample_name)
                    old_experiment = sample_object.experiment
                    sample_object.experiment = new_experiment
                    sample_object.save() 
                    new_archive = ArchiveExperimentSample()
                    new_archive.experiment = old_experiment
                    new_archive.sample = sample_object
                    new_archive.save()
                    #print(new_archive)
        data['form_is_valid'] = True
        samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
        samples_data = get_samples_occupancies(samples)
        data['html_sample_list'] = render_to_string('samples_manager/partial_samples_list.html', {
                                'samples':samples,
                                'samples_data': samples_data,
                                'experiment': experiment
                            })
        return JsonResponse(data)
    else:
        samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
        samples_data = get_samples_occupancies(samples)
        if  logged_user.role == 'Admin': 
                return render(request, 'samples_manager/admin_samples_list.html', {'samples': samples, 'samples_data': samples_data, 'experiment': experiment,'logged_user': logged_user, 'experiments':experiments})
        else:
                return render(request, 'samples_manager/samples_list.html', {'samples': samples,'samples_data': samples_data, 'experiment': experiment,'logged_user': logged_user, 'experiments':experiments})
