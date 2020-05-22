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


def get_experiment_data(experiment):
    if experiment.category == "Passive Standard":
        category_object = get_object_or_404(PassiveStandardCategories, experiment = experiment)
    elif experiment.category == "Passive Custom":
        category_object = get_object_or_404(PassiveCustomCategories, experiment = experiment)
    else:
        category_object = get_object_or_404(ActiveCategories, experiment = experiment)
    requested_fluences = ReqFluences.objects.filter(experiment = experiment)
    materials = Materials.objects.filter(experiment = experiment)
    experiment_samples = Samples.objects.filter(experiment = experiment)
    dosimetry_results =  []
    fluences = []
    for sample in experiment_samples:
        irradiations = Irradiation.objects.filter(sample = sample)
        result = 0 
        tuple_list = []
        for irradiation in irradiations:
            if irradiation.accumulated_fluence:
                if '.' in str(irradiation.dosimeter):
                    print('no calculation') 
                else:
                    dosimeter_area =  irradiation.dosimeter.width * irradiation.dosimeter.height
                    dos_tuple = (dosimeter_area, irradiation.dosimeter, irradiation.accumulated_fluence,irradiation.sample, irradiation.dos_position)
                    tuple_list.append(dos_tuple)
        tuple_list.sort(key=lambda tup: (tup[0],tup[4]))
        if tuple_list:
            sum_fluence = tuple_list[0][2]
            tuple_list_length = len(tuple_list)
            if tuple_list_length> 1:
                for i in range(1,tuple_list_length):
                    if tuple_list[i-1][0] == tuple_list[i][0]:
                        if tuple_list[i-1][4] == tuple_list[i][4]:
                            sum_fluence = sum_fluence + tuple_list[i][2]
                        else:
                            fluences.append({'Sample':sample,'Fluence_data':{'width':tuple_list[i-1][1].width,'height':tuple_list[i-1][1].height,'accumulated_fluence':sum_fluence}})
                            sum_fluence = 0
                    else:
                        fluences.append({'Sample':sample,'Fluence_data':{'width':tuple_list[i-1][1].width,'height':tuple_list[i-1][1].height,'accumulated_fluence':sum_fluence}})
                        sum_fluence = 0

                if tuple_list[tuple_list_length-2][0] == tuple_list[tuple_list_length-1][0]:
                    if tuple_list[i-1][4] == tuple_list[i][4]:
                        fluences.append({'Sample':sample,'Fluence_data':{'width':tuple_list[tuple_list_length-1][1].width,'height':tuple_list[tuple_list_length-1][1].height,'accumulated_fluence':sum_fluence}})
                    else:
                        fluences.append({'Sample':sample,'Fluence_data':{'width':tuple_list[tuple_list_length-1][1].width,'height':tuple_list[tuple_list_length-1][1].height,'accumulated_fluence':tuple_list[tuple_list_length-1][2]}})
                else:
                    fluences.append({'Sample':sample,'Fluence_data':{'width':tuple_list[tuple_list_length-1][1].width,'height':tuple_list[tuple_list_length-1][1].height,'accumulated_fluence':tuple_list[tuple_list_length-1][2]}})
            else:
                 fluences.append({'Sample':sample,'Fluence_data':{'width':tuple_list[tuple_list_length-1][1].width,'height':tuple_list[tuple_list_length-1][1].height,'accumulated_fluence':tuple_list[tuple_list_length-1][2]}})
    data = {'experiment': experiment, 'category_object':category_object, 'requested_fluences':requested_fluences,'materials':materials, 'experiment_samples':experiment_samples, 'fluences':fluences}
    return data


def experiment_details(request, experiment_id):
    experiment = get_object_or_404(Experiments, pk=experiment_id)
    data = get_experiment_data(experiment)
    return render(request, 'samples_manager/experiment_details.html', data)


def admin_experiments_user_view(request, pk):
        logged_user = get_logged_user(request)
        user = Users.objects.get(id = pk)
        experiments = authorised_experiments(user)
        return render(request, 'samples_manager/experiments_list.html', {'experiments': experiments, 'logged_user': logged_user})

def experiments_list(request):
    logged_user = get_logged_user(request)
    if logged_user.role == 'Admin':
        experiments = authorised_experiments(logged_user)
        experiment_data = get_registered_samples_number(experiments)
        return render(request, 'samples_manager/admin_experiments_list.html', {'experiment_data':experiment_data, 'logged_user': logged_user})
    else:
        experiments = authorised_experiments(logged_user)
        return render(request, 'samples_manager/experiments_list.html', {'experiments': experiments, 'logged_user': logged_user})

def admin_experiments_list(request):
    logged_user = get_logged_user(request)
    if logged_user.role == 'Admin':
        experiments = Experiments.objects.order_by('-updated_at')
    else:
        auth_experiments = authorised_experiments(logged_user)
        visible_experiment = True
        for experiment in auth_experiments:
            if experiment.public_experiment == False:
                visible_experiment = False
        if visible_experiment: 
            experiments = Experiments.objects.filter(public_experiment = True)
        else:
            experiments = []
    experiment_data = get_registered_samples_number(experiments)
    return render(request, 'samples_manager/experiments_history.html',{'experiment_data': experiment_data,'logged_user': logged_user})

def experiment_new(request):
    logged_user = get_logged_user(request)
    FluenceFormSet = inlineformset_factory( Experiments, ReqFluences, form=ReqFluencesForm,extra=0, min_num=1,validate_min=True, error_messages="Fluence field is not correctly filled.", formset=ReqFluencesFormSet)
    MaterialFormSet = inlineformset_factory( Experiments,  Materials, form=MaterialsForm, extra=0, min_num=1,validate_min=True, error_messages="Samples type field is not correctly filled.", formset=MaterialsFormSet)
    cern_experiments = Experiments.objects.order_by().values('cern_experiment').distinct()
    cern_experiments_list = []
    for item in cern_experiments:
        cern_experiments_list.append(item['cern_experiment'])
    if request.method == 'POST':
        logging.warning('POST request')
        form1 = ExperimentsForm1(request.POST,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(request.POST)
        form3 = ExperimentsForm3(request.POST)
        fluence_formset = FluenceFormSet(request.POST)
        material_formset = MaterialFormSet(request.POST)
        passive_standard_categories_form =  PassiveStandardCategoriesForm(request.POST)
        passive_custom_categories_form =  PassiveCustomCategoriesForm(request.POST)
        active_categories_form = ActiveCategoriesForm(request.POST)
    else:
        form1 = ExperimentsForm1(data_list=cern_experiments_list,initial={'responsible': logged_user})
        form2 = ExperimentsForm2()
        form3 = ExperimentsForm3()
        fluence_formset = FluenceFormSet()
        material_formset = MaterialFormSet()
        passive_standard_categories_form =  PassiveStandardCategoriesForm()
        passive_custom_categories_form =  PassiveCustomCategoriesForm()
        active_categories_form = ActiveCategoriesForm()
    status = 'new'
    return save_experiment_form_formset(request, form1,form2,form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, status, 'samples_manager/partial_experiment_create.html')

def experiment_status_update(request, pk):
    data = dict()
    logged_user = get_logged_user(request)
    experiment = get_object_or_404(Experiments, pk=pk)
    if request.method == 'POST':
        form =  ExperimentStatus(request.POST,instance=experiment)
        if form.is_valid():
            form.save()
            updated_experiment = Experiments.objects.get(id = experiment.id)
            if  updated_experiment.status == 'Completed':
                message=mark_safe('Dear user,\nyour irradiation experiment with title '+experiment.title+' was completed.\nTwo weeks time is still needed for the cool down. Please, contact us after that period.\n\nKind regards,\nCERN IRRAD team.\nhttps://ps-irrad.web.cern.ch')
                send_mail_notification( 'IRRAD Data Manager: Experiment "%s"  was completed'%experiment.title,message,'irrad.ps@cern.ch', experiment.responsible.email)
                exp_users= updated_experiment.users.values()
                for user in exp_users:
                    send_mail_notification( 'IRRAD Data Manager: Experiment "%s"  was completed'%experiment.title,message,'irrad.ps@cern.ch', user['email'])
            data['form_is_valid'] = True
            if logged_user.role == 'Admin':
                    experiments = Experiments.objects.all().order_by('-updated_at')
                    experiment_data = get_registered_samples_number(experiments)
                    template_data = {'experiment_data': experiment_data}
                    output_template = 'samples_manager/partial_admin_experiments_list.html'
            else: 
                    experiments = authorised_experiments(logged_user)
                    template_data = {'experiments': experiments}
                    output_template = 'samples_manager/partial_experiments_list.html'
            data['html_experiment_list'] = render_to_string(output_template, template_data)
        else:
            print("form is not valid")
    else:
        form = ExperimentStatus(instance=experiment)
    context = {'form': form, 'experiment': experiment}
    data['html_form'] = render_to_string('samples_manager/experiment_status_update.html',
        context,
        request=request,
    )
    return JsonResponse(data)

def experiment_comment_update(request, pk):
    data = dict()
    logged_user = get_logged_user(request)
    experiment = get_object_or_404(Experiments, pk=pk)
    if request.method == 'POST':
        form =   ExperimentComment(request.POST,instance=experiment)
        if form.is_valid():
            form.save()
            output_template = 'samples_manager/partial_experiment_details.html'
            template_data = get_experiment_data(experiment)
            data['html_experiment'] = render_to_string(output_template, template_data)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
            print("form is not valid")
    else:
        form = ExperimentComment(instance=experiment)
    context = {'form': form, 'experiment': experiment}
    data['html_form'] = render_to_string('samples_manager/experiment_comment_update.html',
        context,
        request=request,
    )
    return JsonResponse(data)

def experiment_update(request, pk):
    cern_experiments = Experiments.objects.order_by().values('cern_experiment').distinct()
    cern_experiments_list = []
    for item in cern_experiments:
        cern_experiments_list.append(item['cern_experiment'])
    experiment = get_object_or_404(Experiments, pk=pk)
    FluenceFormSet = inlineformset_factory( Experiments, ReqFluences, form=ReqFluencesForm,extra=0, error_messages="Fluence field is not correctly filled.", formset=ReqFluencesFormSet)
    MaterialFormSet = inlineformset_factory( Experiments, Materials, form=MaterialsForm, extra=0, error_messages="Samples type field is not correctly filled.", formset=MaterialsFormSet)
    if request.method == 'POST':
        form1 = ExperimentsForm1(request.POST, instance=experiment,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(request.POST, instance=experiment)
        form3 = ExperimentsForm3(request.POST, instance=experiment)
        fluence_formset = FluenceFormSet(request.POST, instance=experiment)
        material_formset = MaterialFormSet(request.POST, instance=experiment)
        passive_standard_categories_form = PassiveStandardCategoriesForm(request.POST)
        passive_custom_categories_form = PassiveCustomCategoriesForm(request.POST)
        active_categories_form = ActiveCategoriesForm(request.POST)
        if experiment.category=="Passive Standard": # passive standard
            try:
                cat_instance  = PassiveStandardCategories.objects.get( experiment=experiment)
                passive_standard_categories_form = PassiveStandardCategoriesForm(request.POST,instance = cat_instance)
            except PassiveStandardCategories.DoesNotExist:
                passive_standard_categories_form = PassiveStandardCategoriesForm(request.POST)

        if experiment.category=="Passive Custom": # passive custom
            try:
                cat_instance  = PassiveCustomCategories.objects.get( experiment=experiment)
                passive_custom_categories_form = PassiveCustomCategoriesForm(request.POST,instance = cat_instance)
            except PassiveCustomCategories.DoesNotExist:
                passive_custom_categories_form = PassiveCustomCategoriesForm(request.POST)

        if experiment.category=="Active": # active
            try:
                cat_instance  = ActiveCategories.objects.get( experiment=experiment)
                active_categories_form = ActiveCategoriesForm(request.POST,instance = cat_instance)
            except ActiveCategories.DoesNotExist:
                active_categories_form = ActiveCategoriesForm(request.POST)
    else:
        form1 = ExperimentsForm1(instance=experiment,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(instance=experiment)
        form3 = ExperimentsForm3(instance=experiment)
        fluence_formset = FluenceFormSet(instance=experiment)
        material_formset = MaterialFormSet(instance=experiment)
        passive_standard_categories_form = PassiveStandardCategoriesForm()
        passive_custom_categories_form = PassiveCustomCategoriesForm()
        active_categories_form = ActiveCategoriesForm() 
        if experiment.category=="Passive Standard":
            try:
                cat_instance  = PassiveStandardCategories.objects.get(experiment=experiment)
                passive_standard_categories_form = PassiveStandardCategoriesForm(instance = cat_instance)
            except PassiveStandardCategories.DoesNotExist:
                print("does not exist")
                passive_standard_categories_form = PassiveStandardCategoriesForm()

        if experiment.category=="Passive Custom":
            try:
                cat_instance  = PassiveCustomCategories.objects.get(experiment=experiment)
                passive_custom_categories_form = PassiveCustomCategoriesForm(instance = cat_instance)
            except PassiveCustomCategories.DoesNotExist:
                passive_custom_categories_form = PassiveCustomCategoriesForm()

        if experiment.category=="Active":
            active_categories_form = ActiveCategoriesForm() 
            try:
                cat_instance  = ActiveCategories.objects.get(experiment=experiment)
                active_categories_form = ActiveCategoriesForm(instance = cat_instance)
            except ActiveCategories.DoesNotExist:
                active_categories_form = ActiveCategoriesForm()
    status = 'update'
    return save_experiment_form_formset(request, form1,form2,form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, status, 'samples_manager/partial_experiment_update.html')

def experiment_validate(request, pk):
    cern_experiments = Experiments.objects.order_by().values('cern_experiment').distinct()
    cern_experiments_list = []
    for item in cern_experiments:
        cern_experiments_list.append(item['cern_experiment'])
    experiment = get_object_or_404(Experiments, pk=pk)
    FluenceFormSet = inlineformset_factory( Experiments, ReqFluences, form=ReqFluencesForm,extra=0, error_messages="Fluence field is not correctly filled.", formset=ReqFluencesFormSet)
    MaterialFormSet = inlineformset_factory( Experiments, Materials, form=MaterialsForm, extra=0, error_messages="Samples type field is not correctly filled.", formset=MaterialsFormSet)
    if request.method == 'POST':
        form1 = ExperimentsForm1(request.POST, instance=experiment,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(request.POST, instance=experiment)
        form3 = ExperimentsForm3(request.POST, instance=experiment)
        fluence_formset = FluenceFormSet(request.POST, instance=experiment)
        material_formset = MaterialFormSet(request.POST, instance=experiment)
        passive_standard_categories_form = PassiveStandardCategoriesForm(request.POST)
        passive_custom_categories_form = PassiveCustomCategoriesForm(request.POST)
        active_categories_form = ActiveCategoriesForm(request.POST)
        if experiment.category=="Passive Standard": # passive standard
            try:
                cat_instance  = PassiveStandardCategories.objects.get( experiment=experiment)
                passive_standard_categories_form = PassiveStandardCategoriesForm(request.POST,instance = cat_instance)
            except PassiveStandardCategories.DoesNotExist:
                passive_standard_categories_form = PassiveStandardCategoriesForm(request.POST)

        if experiment.category=="Passive Custom": # passive custom
            try:
                cat_instance  = PassiveCustomCategories.objects.get( experiment=experiment)
                passive_custom_categories_form = PassiveCustomCategoriesForm(request.POST,instance = cat_instance)
            except PassiveCustomCategories.DoesNotExist:
                passive_custom_categories_form = PassiveCustomCategoriesForm(request.POST)

        if experiment.category=="Active": # active
            try:
                cat_instance  = ActiveCategories.objects.get( experiment=experiment)
                active_categories_form = ActiveCategoriesForm(request.POST,instance = cat_instance)
            except ActiveCategories.DoesNotExist:
                active_categories_form = ActiveCategoriesForm(request.POST)
    else:
        form1 = ExperimentsForm1(instance=experiment,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(instance=experiment)
        form3 = ExperimentsForm3(instance=experiment)
        fluence_formset = FluenceFormSet(instance=experiment)
        material_formset = MaterialFormSet(instance=experiment)
        passive_standard_categories_form = PassiveStandardCategoriesForm()
        passive_custom_categories_form = PassiveCustomCategoriesForm()
        active_categories_form = ActiveCategoriesForm() 
        if experiment.category=="Passive Standard":
            try:
                cat_instance  = PassiveStandardCategories.objects.get(experiment=experiment)
                passive_standard_categories_form = PassiveStandardCategoriesForm(instance = cat_instance)
            except PassiveStandardCategories.DoesNotExist:
                print("does not exist")
                passive_standard_categories_form = PassiveStandardCategoriesForm()

        if experiment.category=="Passive Custom":
            try:
                cat_instance  = PassiveCustomCategories.objects.get(experiment=experiment)
                passive_custom_categories_form = PassiveCustomCategoriesForm(instance = cat_instance)
            except PassiveCustomCategories.DoesNotExist:
                passive_custom_categories_form = PassiveCustomCategoriesForm()

        if experiment.category=="Active":
            active_categories_form = ActiveCategoriesForm() 
            try:
                cat_instance  = ActiveCategories.objects.get(experiment=experiment)
                active_categories_form = ActiveCategoriesForm(instance = cat_instance)
            except ActiveCategories.DoesNotExist:
                active_categories_form = ActiveCategoriesForm()
    status = 'validate'
    return save_experiment_form_formset(request, form1,form2,form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, status,'samples_manager/partial_experiment_validate.html')


def experiment_clone(request, pk):
    cern_experiments = Experiments.objects.order_by().values('cern_experiment').distinct()
    cern_experiments_list = []
    for item in cern_experiments:
        cern_experiments_list.append(item['cern_experiment'])
    experiment = get_object_or_404(Experiments, pk=pk)
    FluenceFormSet = inlineformset_factory( Experiments, ReqFluences, form=ReqFluencesForm,extra=0, min_num=1,validate_min=True, error_messages="Fluence field is not correctly filled.", formset=ReqFluencesFormSet)
    MaterialFormSet = inlineformset_factory( Experiments,  Materials, form=MaterialsForm, extra=0, min_num=1,validate_min=True, error_messages="Samples type field is not correctly filled.", formset=MaterialsFormSet)
    if request.method == 'POST':
        form1 = ExperimentsForm1(request.POST, instance=experiment,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(request.POST, instance=experiment)
        form3 = ExperimentsForm3(request.POST, instance=experiment)
        fluence_formset = FluenceFormSet(request.POST)
        material_formset = MaterialFormSet(request.POST)
        passive_standard_categories_form = PassiveStandardCategoriesForm(request.POST)
        passive_custom_categories_form = PassiveCustomCategoriesForm(request.POST)
        active_categories_form = ActiveCategoriesForm(request.POST)
    else:
        form1 = ExperimentsForm1(instance=experiment,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(instance=experiment)
        form3 = ExperimentsForm3(instance=experiment)
        fluence_formset = FluenceFormSet()
        material_formset = MaterialFormSet()
        passive_standard_categories_form = PassiveStandardCategoriesForm()
        passive_custom_categories_form = PassiveCustomCategoriesForm()
        active_categories_form = ActiveCategoriesForm() 
    status = 'clone'
    return save_experiment_form_formset(request, form1,form2,form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, status, 'samples_manager/partial_experiment_clone.html')



def save_experiment_form_formset(request,form1, form2, form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, status, template_name):
    data = dict()
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        if status == 'new' or  status == 'clone': # status experiment
            if form1.is_valid() and form2.is_valid() and form3.is_valid() and fluence_formset.is_valid() and material_formset.is_valid():
                if form1.checking_unique() == True:
                    experiment_data = {}
                    experiment_data.update(form1.cleaned_data)
                    experiment_data.update(form2.cleaned_data)
                    experiment_data.update(form3.cleaned_data)
                    experiment_temp = Experiments.objects.create(**experiment_data)
                    experiment = Experiments.objects.get(pk = experiment_temp.pk)
                    experiment.created_by =  logged_user 
                    experiment.updated_by =  logged_user
                    experiment.status = "Registered"
                    experiment.save()
                    print("experiment saved")
                    if experiment.category == "Passive Standard":
                        if passive_standard_categories_form.is_valid(): 
                            if passive_standard_categories_form.cleaned_data is not None:
                                passive_standard_category = passive_standard_categories_form.save()
                                passive_standard_category.experiment = experiment
                                passive_standard_category.save()
                    elif  experiment.category == "Passive Custom":
                        if passive_custom_categories_form.is_valid(): 
                            if  passive_custom_categories_form.cleaned_data is not None:
                                passive_custom_category = passive_custom_categories_form.save()
                                passive_custom_category.experiment = experiment
                                passive_custom_category.save()
                    elif  experiment.category == "Active":
                        if active_categories_form.is_valid(): 
                            if active_categories_form.cleaned_data is not None:
                                active_category = active_categories_form.save()
                                active_category.experiment = experiment
                                active_category.save()
                    else: 
                        print("no category")
                    if fluence_formset.is_valid():
                        if fluence_formset.cleaned_data is not None:
                            for form in fluence_formset.forms:
                                fluence = form.save()
                                fluence.experiment = experiment
                                fluence.save()
                        else:
                            print("data none")
                    else:
                        print("fluence not valid")
                    print(fluence_formset.is_valid())
                    if material_formset.is_valid():
                        if material_formset.cleaned_data is not None:
                            for form in material_formset.forms:
                                material= form.save()
                                material.experiment = experiment
                                material.save()
                    else:
                        print("material formset not valid")
                    if  status == 'clone':
                        previous_experiment = Experiments.objects.get(pk =  form1.instance.pk)
                        for user in previous_experiment.users.all():
                            experiment.users.add(user)
                    data['form_is_valid'] = True
                    if logged_user.role == 'Admin':
                        experiments = Experiments.objects.all().order_by('-updated_at')
                        experiment_data = get_registered_samples_number(experiments)
                        template_data = {'experiment_data': experiment_data}
                        output_template = 'samples_manager/partial_admin_experiments_list.html'
                    else: 
                        experiments = authorised_experiments(logged_user)
                        template_data = {'experiments': experiments}
                        output_template = 'samples_manager/partial_experiments_list.html'
                    data['html_experiment_list'] = render_to_string(output_template, template_data)
                    data['state'] = "Created"
                    message=mark_safe('Dear user,\nyour irradiation experiment with title: '+experiment.title+' was successfully registered by this account: '+logged_user.email+'.\nPlease, find all your experiments at this URL: http://cern.ch/irrad.data.manager/samples_manager/experiments/\nIn case you believe that this e-mail has been sent to you by mistake please contact us at irrad.ps@cern.ch.\nKind regards,\nCERN IRRAD team.\nhttps://ps-irrad.web.cern.ch')
                    send_mail_notification( 'IRRAD Data Manager: New experiment registered in the CERN IRRAD Proton Irradiation Facility',message,'irrad.ps@cern.ch', experiment.responsible.email)
                    message2irrad=mark_safe("The user with the account: "+logged_user.email+" registered a new experiment with title: "+ experiment.title+".\nPlease, find all the registerd experiments in this link: https://irrad-data-manager.web.cern.ch/samples_manager/experiments/")
                    send_mail_notification('IRRAD Data Manager: New experiment',message2irrad,logged_user.email,'irrad.ps@cern.ch')
                else:
                    data['form_is_valid'] = False
                    data['state'] = "not unique"
                    print("not unique")
            else:
                print("form1: ",form1.is_valid())
                print("form2: ",form2.is_valid())
                print("form3: ",form3.is_valid())
                print("fluence: ",fluence_formset.is_valid())
                print(fluence_formset)
                print("material_formset: ",material_formset.is_valid())
                print(material_formset)
                data['form_is_valid'] = False
                data['state'] = "missing fields"
                print("not valid")
        elif  status == 'update':
            print("update")
            if form1.is_valid() and form2.is_valid() and form3.is_valid():
                old_experiment = Experiments.objects.get(pk =  form1.instance.pk)
                old_fluences = ReqFluences.objects.all().filter(experiment = form1.instance.pk).order_by('id')
                old_materials = Materials.objects.all().filter(experiment = form1.instance.pk).order_by('id')
                for f in  old_fluences: 
                    pass
                for m in  old_materials: 
                    pass
                experiment_updated = form1.save()
                form2.save()
                form3.save()
                experiment = Experiments.objects.get(pk =  experiment_updated.pk)
                experiment.updated_by = logged_user
                experiment.save()
                if experiment.category == "Passive Standard":
                    if passive_standard_categories_form.is_valid(): 
                        old_category = PassiveStandardCategories.objects.get(experiment =  form1.instance.pk)
                        if passive_standard_categories_form.cleaned_data is not None:
                            passive_standard_category = passive_standard_categories_form.save()
                            passive_standard_category.experiment = experiment
                            passive_standard_category.save()
                elif  experiment.category == "Passive Custom":
                    old_category = PassiveCustomCategories.objects.get(experiment =  form1.instance.pk)
                    if passive_custom_categories_form.is_valid(): 
                        if  passive_custom_categories_form.cleaned_data is not None:
                            passive_custom_category = passive_custom_categories_form.save()
                            passive_custom_category.experiment = experiment
                            passive_custom_category.save()
                elif  experiment.category == "Active":
                    old_category = ActiveCategories.objects.get(experiment =  form1.instance.pk)
                    if active_categories_form.is_valid(): 
                        if active_categories_form.cleaned_data is not None:
                            active_category = active_categories_form.save()
                            active_category.experiment = experiment
                            active_category.save()
                else: 
                    print("no category")
                if fluence_formset.is_valid():
                    fluence_formset.save()
                else:
                    print("fluence not valid!!!!!")
                if  material_formset.is_valid():    
                    material_formset.save()
                data['form_is_valid'] = True
                if logged_user.role == 'Admin':
                    experiments = Experiments.objects.all().order_by('-updated_at')
                    experiment_data = get_registered_samples_number(experiments)
                    template_data = {'experiment_data': experiment_data, 'logged_user': logged_user}
                    output_template = 'samples_manager/partial_admin_experiments_list.html'
                else: 
                    experiments = authorised_experiments(logged_user)
                    template_data = {'experiments': experiments}
                    output_template = 'samples_manager/partial_experiments_list.html'
                data['html_experiment_list'] = render_to_string(output_template, template_data)
                data['state'] = "Updated"
                text = updated_experiment_data(old_experiment,old_fluences,old_materials,old_category,experiment)
                message2irrad=mark_safe("The user with e-mail: "+logged_user.email+" updated the experiment with title '"+experiment.title+"'.\n"
                +"The updated fields are: \n"+text+"\nPlease, find all the experiments in this link: https://irrad-data-manager.web.cern.ch/samples_manager/experiments/")
                send_mail_notification('IRRAD Data Manager: Updated experiment',message2irrad,logged_user.email,'irrad.ps@cern.ch')
            else:
                print("form1: ",form1.is_valid())
                print("form2: ",form2.is_valid())
                print("form3: ",form3.is_valid())
                print("fluence: ",fluence_formset.is_valid())
                print(fluence_formset)
                print("material_formset: ",material_formset.is_valid())
                print(material_formset)
                data['form_is_valid'] = False
                data['state'] = "missing fields"
                print("not valid")
        elif  status == 'validate':  # validation
            print("validation")
            if form1.is_valid() and form2.is_valid() and form3.is_valid():
                experiment_updated = form1.save()
                form2.save()
                form3.save()
                experiment = Experiments.objects.get(pk =  experiment_updated.pk)
                experiment.status = "Validated"
                experiment.updated_by = logged_user
                experiment.save()
                if experiment.category == "Passive Standard":
                    if passive_standard_categories_form.is_valid(): 
                        if passive_standard_categories_form.cleaned_data is not None:
                            passive_standard_category = passive_standard_categories_form.save()
                            passive_standard_category.experiment = experiment
                            passive_standard_category.save()
                elif  experiment.category == "Passive Custom":
                    if passive_custom_categories_form.is_valid(): 
                        if  passive_custom_categories_form.cleaned_data is not None:
                            passive_custom_category = passive_custom_categories_form.save()
                            passive_custom_category.experiment = experiment
                            passive_custom_category.save()
                elif  experiment.category == "Active":
                    if active_categories_form.is_valid(): 
                        if active_categories_form.cleaned_data is not None:
                            active_category = active_categories_form.save()
                            active_category.experiment = experiment
                            active_category.save()
                else: 
                    print("no category")
                if fluence_formset.is_valid():
                    fluence_formset.save()
                else:
                    print("fluence not valid")
                    print(fluence_formset)
                if  material_formset.is_valid():   
                    material_formset.save()
                data['form_is_valid'] = True
                experiments = Experiments.objects.all().order_by('-updated_at')
                experiment_data = get_registered_samples_number(experiments)
                data['state'] = "Validated"
                data['html_experiment_list'] = render_to_string('samples_manager/partial_admin_experiments_list.html', {
                            'experiment_data':  experiment_data, 'logged_user':logged_user 
                        })
                message='Dear user,\nyour experiment with title "%s" was validated. \nYou can now add samples and additional users related to your irradiation experiment.\nPlease, find all your experiments in this link: https://irrad-data-manager.web.cern.ch/samples_manager/experiments/\n\nKind regards,\nCERN IRRAD team.\nhttps://ps-irrad.web.cern.ch'% experiment.title
                send_mail_notification('IRRAD Data Manager: Experiment  %s validation' % experiment.title,message,'irrad.ps@cern.ch',experiment.responsible.email)
                message2irrad='You validated the experiment with title: %s' % experiment.title
                send_mail_notification('IRRAD Data Manager: Experiment %s validation' % experiment.title,message2irrad,'irrad.ps@cern.ch','irrad.ps@cern.ch')
            else:
                print("form1: ",form1.is_valid())
                print("form2: ",form2.is_valid())
                print("form3: ",form3.is_valid())
                print("fluence: ",fluence_formset.is_valid())
                print(fluence_formset)
                print("material_formset: ",material_formset.is_valid())
                print(material_formset)
                data['form_is_valid'] = False
                data['state'] = "missing fields"
                print("not valid")
        else:
            print("nothing to do")
        
    context = {'form1': form1,'form2': form2, 'form3': form3, 'fluence_formset': fluence_formset, 'material_formset': material_formset, 'passive_standard_categories_form': passive_standard_categories_form, 'passive_custom_categories_form': passive_custom_categories_form, 'active_categories_form': active_categories_form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    print("all saved!")
    return JsonResponse(data)


def experiment_delete(request, pk):
    experiment = get_object_or_404(Experiments, pk=pk)
    data = dict()
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        experiment.delete()
        data['form_is_valid'] = True
        if logged_user.role == 'Admin':
                experiments = Experiments.objects.all().order_by('-updated_at')
                experiment_data = get_registered_samples_number(experiments)
                template_data = { 'experiment_data': experiment_data }
                output_template = 'samples_manager/partial_admin_experiments_list.html'
        else: 
                experiments = authorised_experiments(logged_user)
                template_data = { 'experiments': experiments }
                output_template = 'samples_manager/partial_experiments_list.html'
        data['html_experiment_list'] = render_to_string(output_template, template_data)
        data['state']='Deleted'
        message=mark_safe('Dear user,\nyour irradiation experiment with title '+experiment.title+' was deleted by the account: '+logged_user.email+'.\nPlease, find all your experiments at this URL: http://cern.ch/irrad.data.manager/samples_manager/experiments/\n\nKind regards,\nCERN IRRAD team.\nhttps://ps-irrad.web.cern.ch')
        send_mail_notification( 'IRRAD Data Manager: Experiment "%s"  was deleted'%experiment.title,message,'irrad.ps@cern.ch', experiment.responsible.email)
        message2irrad=mark_safe("The user with the account: "+logged_user.email+" deleted the experiment with title '"+ experiment.title+"'.\n")
        send_mail_notification( 'IRRAD Data Manager: Experiment "%s"  was deleted'%experiment.title,message2irrad,experiment.responsible.email, 'irrad.ps@cern.ch')
    else:
        context = {'experiment': experiment}
        data['html_form'] = render_to_string('samples_manager/partial_experiment_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def change_experiment_visibility(request, pk):
    data = dict()
    try:
        experiment = Experiments.objects.get(id = pk)
        full_path = request.get_full_path()
        change = full_path.split("/")[6]
        if change == 'on':
            experiment.public_experiment = True
        else:
            experiment.public_experiment = False
        experiment.save()
        data['request_valid'] = True
        data['experiment_visibility'] = render_to_string('samples_manager/experiment_visibility.html', {
                    'experiment':experiment,
                }) 
    except: 
        data['request_valid'] = False 
    return JsonResponse(data)


def updated_experiment_data(old_experiment,old_fluences,old_materials,old_category,new_experiment):
    excluded_keys = 'id', 'status', 'responsible', 'users', 'created_at', 'updated_at', 'created_by','updated_by', '_state'
    old_dict, new_dict = old_experiment.__dict__, new_experiment.__dict__
    experiment_flag, category_flag, fluence_flag, material_flag = False, False, False, False
    text = ""
    for k,v in old_dict.items():
            if k in excluded_keys:
                continue
            try:
                if v != new_dict[k]:
                    experiment_flag = True
                    text = text + str(k)+": "+ str(new_dict[k])+" (old value: "+str(old_dict[k])+") \n"
            except KeyError:
                print("key error")
    category_text = "\nCategories:\n"
    category_excluded_keys = 'id', 'experiment_id', '_state'
    if new_experiment.category =="Passive Standard":
        new_category = PassiveStandardCategories.objects.get(experiment = new_experiment)
        old_category_dict, new_category_dict = old_category.__dict__, new_category.__dict__ 
        for k,v in old_category_dict.items():
            if k in excluded_keys:
                continue
            try:
                if v != new_category_dict[k]:
                    category_flag = True
                    category_text = category_text + str(k)+"\n"
            except KeyError:
                print("key error")
    elif new_experiment.category =="Passive Custom":
        new_category = PassiveCustomCategories.objects.get(experiment = new_experiment)
        old_category_dict, new_category_dict = old_category.__dict__, new_category.__dict__ 
        for k,v in old_category_dict.items():
            if k in excluded_keys:
                continue
            try:
                if v != new_category_dict[k]:
                    category_flag = True
                    category_text = category_text + str(k)+": "+ str(new_category_dict[k])+" (old value: "+str(old_category_dict[k])+") \n"
            except KeyError:
                print("key error")
    elif new_experiment.category =="Active":
        new_category = ActiveCategories.objects.get(experiment = new_experiment)
        old_category_dict, new_category_dict = old_category.__dict__, new_category.__dict__ 
        for k,v in old_category_dict.items():
            if k in excluded_keys:
                continue
            try:
                if v != new_category_dict[k]:
                    category_flag = True
                    category_text = category_text + str(k)+": "+ str(new_category_dict[k])+" (old value: "+str(old_category_dict[k])+") \n"
            except KeyError:
                print("key error")
    old_fluences_number = len(old_fluences)
    new_fluences = ReqFluences.objects.filter(experiment = new_experiment).order_by('id') 
    new_fluences_number = len(new_fluences)
    fluences_text="\nFluences: \n"
    old_fluence_ids = []
    new_fluence_ids = []
    for f in new_fluences:
        new_fluence_ids.append(f.id)
    fluences_after_removal = []
    for fluence in old_fluences:
        if fluence.id not in new_fluence_ids:
            fluence_flag = True
            fluences_text =  fluences_text +"value "+ str(fluence.req_fluence) +" was removed\n"
        else:
            fluences_after_removal.append(fluence)
    for f in fluences_after_removal:
        old_fluence_ids.append(f.id)
    i=0
    for fluence in new_fluences: # checking for edited fluences or newly added
        if fluence.id in old_fluence_ids:
            if fluence.req_fluence != fluences_after_removal[i].req_fluence:
                fluence_flag = True
                fluences_text =  fluences_text + str(fluence.req_fluence) + "(old value: "+str(fluences_after_removal[i].req_fluence)+")\n"
            else:
                pass
            i= i+1
        else:
            fluence_flag = True
            fluences_text =  fluences_text + str(fluence.req_fluence)+ " (New added value)\n"

    old_materials_number = len(old_materials)
    new_materials = Materials.objects.filter(experiment = new_experiment).order_by('id') 
    new_materials_number = len(new_materials)
    materials_text="\nSample types: \n"
    old_material_ids = []
    new_material_ids = []
    for m in new_materials:
        new_material_ids.append(m.id)
    materials_after_removal = []
    for material in old_materials:
        if material.id not in new_material_ids:
            material_flag = True
            materials_text =  materials_text +"value "+ str(material.material) +" was removed\n"
        else:
            materials_after_removal.append(material)

    for m in materials_after_removal:
        old_material_ids.append(m.id)
    i=0
    for material in new_materials: # checking for edited materials or newly added
        if material.id in old_material_ids:
            if material.material != materials_after_removal[i].material:
                material_flag = True
                materials_text =  materials_text + str(material.material) + "(old value: "+str(materials_after_removal[i].material)+")\n"
            else:
                pass
            i = i + 1
        else:
            material_flag = True
            materials_text =  materials_text + str(material.material)+ " (New added value)\n"

    if category_flag == True:
        text = text + category_text
    else:
        pass
    if fluence_flag == True:
        text = text + fluences_text 
    else:
        pass
    if material_flag == True:
        text = text + materials_text  
    else:
        pass 
    return text