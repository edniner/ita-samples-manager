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



def save_compound_form(request, form, elem_formset, experiment, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid() and elem_formset.is_valid():
            compound = form.save()
            if elem_formset.is_valid():
                if elem_formset.cleaned_data is not None:
                        for form in elem_formset.forms:
                            element = form.save()
                            element.compound = compound
                            element.save()
                            print("in element form")
                else:
                            print("data none")
            data['form_is_valid'] = True
            context = {}
            data['compound_id'] = compound.id
            data['compound_name'] = compound.name
        else:
            data['form_is_valid'] = False
    else:
        context = {'form': form, 'elem_formset': elem_formset,'experiment': experiment}
        data['html_form'] = render_to_string(template_name, context, request=request)
    print("I'm here!!")
    return JsonResponse(data)

def save_admin_compound_form(request,form,elem_formset,status,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid() and elem_formset.is_valid():
            compound = form.save()
            if elem_formset.cleaned_data is not None:
                for form in elem_formset.forms:
                    element = form.save()
                    element.compound = compound
                    element.save()
                    '''for e in element:
                            print(e.compound)
                        for elem in elem_formset.forms:
                            print(elem.cleaned_data['percentage'])
                            sum = sum + elem.cleaned_data['percentage']
                        if sum == 100:
                            compound = form.save()
                            for elem in elem_formset.forms:
                                element = elem.save()
                                element.compound = compound
                                element.save()
                            compounds_data = get_compounds_data()
                            data['html_compound_list'] = render_to_string('samples_manager/partial_compounds_list.html', {
                                        'compounds_data':compounds_data,
                                })
                            data['form_is_valid'] = True
                            data['state'] = "ok"
                        else:
                            print("data not ok!")
                            data['state'] = "sum not ok"
                            data['form_is_valid'] = False'''
                compounds_data = get_compounds_data()
                data['html_compound_list'] = render_to_string('samples_manager/partial_compounds_list.html', {
                        'compounds_data':compounds_data,
                })
                data['form_is_valid'] = True
                data['state'] = "ok"
            else:
                print("data none")
                data['state'] = "no data"
                data['form_is_valid'] = False
        else:
            if form.is_valid() and status =='update':
                form.save()
                compounds_data = get_compounds_data()
                data['html_compound_list'] = render_to_string('samples_manager/partial_compounds_list.html', {
                                        'compounds_data':compounds_data,
                                })
                data['form_is_valid'] = True
                data['state'] = "ok"
            else:
                data['form_is_valid'] = False
                data['state'] = "not valid"
                print("form not valid!")
    context = {'form': form, 'elem_formset': elem_formset}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def compound_new(request, experiment_id):
    logged_user = get_logged_user(request)
    experiment = Experiments.objects.get(pk = experiment_id)
    ElemFormSet = inlineformset_factory(Compound, CompoundElements, form=CompoundElementsForm,extra=0, min_num=1,validate_min=True, error_messages="Compound is not filled", formset=CompoundElementsFormSet)
    if request.method == 'POST':
        form = CompoundForm(request.POST)
        elem_formset = ElemFormSet(request.POST)
    else:
        form = CompoundForm()
        elem_formset = ElemFormSet()
    return save_compound_form(request, form, elem_formset, experiment, 'samples_manager/partial_compound_create.html' )

def admin_compound_new(request):
    logged_user = get_logged_user(request)
    ElemFormSet = inlineformset_factory(Compound, CompoundElements, form=CompoundElementsForm,extra=0, min_num=1,validate_min=True, error_messages="Compound is not filled", formset=CompoundElementsFormSet)
    if request.method == 'POST':
        form = CompoundForm(request.POST)
        elem_formset = ElemFormSet(request.POST)
    else:
        form = CompoundForm()
        elem_formset = ElemFormSet()
    status = 'new'
    return save_admin_compound_form(request, form, elem_formset, status,'samples_manager/admin_partial_compound_create.html' )


def admin_compound_update(request, pk):
    compound = get_object_or_404(Compound, pk=pk)
    ElemFormSet = inlineformset_factory(Compound, CompoundElements, form=CompoundElementsForm,extra=0, error_messages="Compound is not filled", formset=CompoundElementsFormSet)
    if request.method == 'POST':
        form = CompoundForm(request.POST, instance = compound)
        elem_formset = ElemFormSet(request.POST,  instance = compound)
    else:
        form = CompoundForm(instance = compound)
        elem_formset = ElemFormSet(instance = compound)
    status = 'update'
    return save_admin_compound_form(request,form, elem_formset, status, 'samples_manager/admin_partial_compound_update.html' )

def admin_compound_delete(request, pk):
    compound = get_object_or_404(Compound, pk=pk)
    data = dict()
    if request.method == 'POST':
        compound.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        compounds_data = get_compounds_data()
        data['html_compound_list'] = render_to_string('samples_manager/partial_compounds_list.html', {
                                        'compounds_data':compounds_data,
        })
    else:
        context = {'compound': compound}
        data['html_form'] = render_to_string('samples_manager/admin_partial_compound_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def compound_samples_list(compound):
     layers = Layers.objects.filter(compound_type = compound)
     compound_samples = []
     samples_sum = 0
     for layer in layers:
         compound_samples.append(layer.sample)
         samples_sum = samples_sum + 1 
     return samples_sum

def get_compounds_data():
    compounds = Compound.objects.all()
    compounds_data = []
    for compound in compounds:
        samples_sum = compound_samples_list(compound)
        compounds_data.append({
            "compound":compound,
            "samples_sum":samples_sum,
            })
    return compounds_data

def compounds_list(request):
    logged_user = get_logged_user(request)
    compounds_data = get_compounds_data()
    return render(request, 'samples_manager/compounds_list.html',{'compounds_data': compounds_data,'logged_user': logged_user})
