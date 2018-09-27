# layer deleting doesn't work well to be checked!!!!
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Experiments,ReqFluences, Materials,PassiveStandardCategories,PassiveCustomCategories,ActiveCategories,Users,Samples,Compound,CompoundElements, Layers, Dosimeters,Irradiation, ArchiveExperimentSample, Occupancies
from django.template import loader
from django.core.urlresolvers import reverse
import datetime
from .forms import *
#from .forms import CompoundFormset, ExperimentsForm1,ExperimentsForm2,ExperimentsForm3, UsersForm, ReqFluencesForm, MaterialsForm, PassiveStandardCategoriesForm, PassiveCustomCategoriesForm,ActiveCategoriesForm, SamplesForm1, SamplesForm2,CompoundElementsForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from django.utils.safestring import mark_safe
import logging 
from django.db.models import Q
from django.utils import timezone
import re



def send_mail_notification(title,message,from_mail,to_mail):
    headers = {'Reply-To': 'irrad.ps@cern.ch'}
    from_mail='irrad.ps@cern.ch'
    msg = EmailMessage(title,message,from_mail, to=[to_mail], headers = headers)
    msg.send()

def get_logged_user(request):
    username =  request.META["HTTP_X_REMOTE_USER"]
    firstname = request.META["HTTP_X_REMOTE_USER_FIRSTNAME"]
    lastname = request.META["HTTP_X_REMOTE_USER_LASTNAME"]
    telephone = request.META["HTTP_X_REMOTE_USER_PHONENUMBER"]
    email =  request.META["HTTP_X_REMOTE_USER_EMAIL"]
    mobile = request.META["HTTP_X_REMOTE_USER_MOBILENUMBER"]
    department = request.META["HTTP_X_REMOTE_USER_DEPARTMENT"] 
    home_institute = request.META["HTTP_X_REMOTE_USER_HOMEINSTITUTE"]

    '''username =  "bgkotse"
    firstname =  "Ina"
    lastname = "Gkotse"
    telephone = "11111"
    #email =  "Blerina.Gkotse@telecom-bretagne.eu"
    email =  "Blerina.Gkotse@cern.ch"
    mobile = "12345"
    department = "EP/DT"
    home_institute = "MINES ParisTech"'''
    
    email =  email.lower()
    users = Users.objects.all()
    emails = []
    for item in users:
        emails.append(item.email)
    if not email in emails:
        new_user = Users()
        if firstname is not None:
            new_user.name = firstname
        if lastname is not None:
            new_user.surname = lastname
        if mobile:
            new_user.telephone = mobile
            new_user.db_telephone = mobile
        else:
            new_user.telephone = telephone
            new_user.db_telephone = telephone
        if email is not None:
            new_user.email = email
        logged_user =  new_user
    else:
        logged_user = Users.objects.get( email = email)

    if mobile:
        logged_user.db_telephone = mobile
    else:
        logged_user.db_telephone = telephone
    if department:
         logged_user.department =  department

    if home_institute:
        logged_user.home_institute = home_institute
    logged_user.last_login = timezone.now()
    logged_user.save()
    return logged_user
    

def index(request):
    template = loader.get_template('samples_manager/index.html')
    logged_user = get_logged_user(request)
    context = {'logged_user': logged_user}
    return render(request, 'samples_manager/index.html', context)


def view_user(request):
    #only in production
    logged_user = get_logged_user(request)
    #logged_user = 'blerina.gkotse@cern.ch'
    html = "<html><body><div id='user_id'>User e-mail %s.</div></body></html>" %  logged_user.email
    return HttpResponse(html)

def regulations(request):
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/terms_conditions.html', {'logged_user': logged_user})

def fluence_conversion(request):
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/fluence_conversion.html', {'logged_user': logged_user})

def get_registered_samples_number(experiments):
    experiment_data = []
    total_registered_samples = 0
    total_declared_samples = 0
    total_experiments_radiation_length_occupancy = 0
    total_experiments_nu_coll_length_occupancy = 0
    total_experiments_int_length_occupancy = 0
    row = 0
    for experiment in experiments:
            samples = Samples.objects.filter(experiment = experiment)
            number = samples.count()
            total_radiation_length_occupancy = 0
            total_nu_coll_length_occupancy = 0
            total_nu_int_length_occupancy = 0
            for sample in samples:
                occupancy = Occupancies.objects.filter(sample=sample)
                if len(occupancy) == 0:
                    save_occupancies(sample,"new")
                    occupancy = Occupancies.objects.filter(sample=sample)
                if len(occupancy) != 0:
                    total_radiation_length_occupancy = total_radiation_length_occupancy + occupancy[0].radiation_length_occupancy
                    total_nu_coll_length_occupancy = total_nu_coll_length_occupancy + occupancy[0].nu_coll_length_occupancy
                    total_nu_int_length_occupancy = total_nu_int_length_occupancy + occupancy[0].nu_int_length_occupancy
                else:
                    pass
            total_registered_samples = total_registered_samples + number
            total_declared_samples = total_declared_samples + int(experiment.number_samples)
            row = row + 1
            experiment_data.append({  
            "experiment": experiment,
            "number_samples": number,
            "row":row,
            "total_radiation_length_occupancy": total_radiation_length_occupancy,
            "total_nu_coll_length_occupancy": total_nu_coll_length_occupancy,
            "total_nu_int_length_occupancy": total_nu_int_length_occupancy,
            })
            total_experiments_radiation_length_occupancy = total_experiments_radiation_length_occupancy + total_radiation_length_occupancy
            total_experiments_nu_coll_length_occupancy = total_experiments_nu_coll_length_occupancy + total_nu_coll_length_occupancy
            total_experiments_int_length_occupancy = total_experiments_int_length_occupancy + total_nu_int_length_occupancy
    data = {
            "experiments":experiment_data,"total_registered_samples": total_registered_samples,"total_declared_samples": total_declared_samples,
            "total_experiments_radiation_length_occupancy": total_experiments_radiation_length_occupancy,
            "total_experiments_nu_coll_length_occupancy": total_experiments_nu_coll_length_occupancy,
            "total_experiments_int_length_occupancy": total_experiments_int_length_occupancy
            }
    return data


def get_layers(experiment):
    samples = Samples.objects.filter(experiment = experiment)
    for sample in samples:
        layers = Layers.objects.filter(sample = sample)
        for layer in layers:
            layer_length = layer.length
            element_type = str(layer.element_type)
            element = element_type.split("(")[0]
            x = 0 
            if layer.percentage < 100:
                pass    #compound
            else:
                x = layer.length 
            x_layer = x / layer.density
            x_layer_trunc = '%.6f'%(x_layer)

def authorised_experiments(logged_user):
     if logged_user.role == 'Admin':
        experiments = Experiments.objects.order_by('-updated_at')
     else:
         experiment_values = Experiments.objects.filter(Q(users=logged_user)|Q(responsible=logged_user)).values('title').distinct()
         experiments = []
         for value in experiment_values:
             experiment = Experiments.objects.get(title = value['title'])
             experiments.append(experiment)
     return experiments

def filtered_authorised_experiments(logged_user, experiments):
    if logged_user.role != 'Admin':
         experiment_values = experiments.filter(Q(users=logged_user)|Q(responsible=logged_user)).values('title').distinct()
         authorised_experiments = []
         for value in experiment_values:
             experiment = experiments.get(title = value['title'])
             authorised_experiments.append(experiment)
         return authorised_experiments
    else:
        return experiments 

def irradiations(request):
     logged_user = get_logged_user(request)
     irradiations = []
     if logged_user.role == 'Admin':
        irradiations = Irradiation.objects.all()
     return render(request, 'samples_manager/irradiations_list.html', {'irradiations': irradiations, 'logged_user': logged_user})

def experiments_list(request):
    preference = request.session.get('registered_preferences', 'amazon')
    print("selected ",preference)
    logged_user = get_logged_user(request)
    form = PreferencesForm(initial={'global_theme':'amazon' })
    print(form)
    if logged_user.role == 'Admin':
        experiments = authorised_experiments(logged_user)
        experiment_data = get_registered_samples_number(experiments)
        return render(request, 'samples_manager/admin_experiments_list.html', {'experiment_data':experiment_data, 'logged_user': logged_user, 'form': form})
    else:
        experiments = authorised_experiments(logged_user)
        return render(request, 'samples_manager/experiments_list.html', {'experiments': experiments, 'logged_user': logged_user})

def register_preferences(request):
    print("registered preferences!!")
    preference = request.POST.get('global_theme')
    request.session['registered_preferences'] = preference
    data = dict()
    data['option'] = preference
    return JsonResponse(data)


def admin_experiments_user_view(request, pk):
        logged_user = get_logged_user(request)
        user = Users.objects.get(id = pk)
        experiments = authorised_experiments(user)
        return render(request, 'samples_manager/experiments_list.html', {'experiments': experiments, 'logged_user': logged_user})


def admin_experiments_list(request):
    experiments = Experiments.objects.order_by('-updated_at')
    experiment_data = get_registered_samples_number(experiments)
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/admin_experiments_list.html', {'experiment_data': experiment_data,'logged_user': logged_user})

def users_list(request):
    logged_user = get_logged_user(request)
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
    return render(request, 'samples_manager/admin_users_list.html', {'users_data': users_data,'logged_user': logged_user})


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

def user_details(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    return render(request, 'samples_manager/user_details.html', {'user': user})


def irradiation_new(request):
    data = dict()
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        form = IrradiationForm(request.POST)
        if form.is_valid():
            irradiation = form.save()
            irradiation.status = "Registered"
            irradiation.save()
            irradiations = Irradiation.objects.all()
            data['form_is_valid'] = True
            data['html_irradiation_list'] = render_to_string('samples_manager/partial_irradiations_list.html',{'irradiations': irradiations, 'logged_user': logged_user})
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
        form = IrradiationFormEdit(request.POST, instance = irradiation)
        if form.is_valid():
            form.save()
            irradiations = Irradiation.objects.all()
            data['form_is_valid'] = True
            data['html_irradiation_list'] = render_to_string('samples_manager/partial_irradiations_list.html',{'irradiations': irradiations, 'logged_user': logged_user})
        else:
            data['form_is_valid'] = False
    else:
        form = IrradiationFormEdit(instance = irradiation)
        context = {'form': form, 'logged_user': logged_user}
        data['html_form'] = render_to_string('samples_manager/partial_irradiation_form.html',
                    context,
                    request=request,
                )
    return JsonResponse(data)

def irradiation_delete(request ,pk):
    irradiation = get_object_or_404(Irradiation, pk=pk)
    logged_user = get_logged_user(request)
    data = dict()
    if request.method == 'POST':
        irradiation.delete()
        data['form_is_valid'] = True 
        irradiations = Irradiation.objects.all()
        data['html_irradiation_list'] = render_to_string('samples_manager/partial_irradiations_list.html',
        {'irradiations': irradiations, 'logged_user': logged_user})
    else:
        context = {'irradiation': irradiation,}
        data['html_form'] = render_to_string('samples_manager/partial_irradiation_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)


def new_group_irradiation(request, experiment_id):
    data = dict()
    print("new_irradiation")
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
    print("before rendering")
    data['html_form'] = render_to_string('samples_manager/partial_group_irradiation_form.html', context, request=request)
    print("selected:",selected_samples)
    return JsonResponse(data)


def assign_dosimeters(request, experiment_id):
    data = dict()
    print("assign dosimeters")
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
                        irradiation = Irradiation()
                        irradiation.sample = sample
                        irradiation.dosimeter = dosimeter
                        irradiation.irrad_table = form.cleaned_data['irrad_table']
                        irradiation.table_position = form.cleaned_data['table_position']
                        irradiation.status = "Registered"
                        irradiation.updated_by = logged_user
                        irradiation.created_by = logged_user
                        irradiation.save()
            irradiations = Irradiation.objects.all()
            data['form_is_valid'] = True
            data['html_irradiation_list'] = render_to_string('samples_manager/irradiations_list.html',{'irradiations': irradiations, 'logged_user': logged_user})
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



def assign_samples_dosimeters(request):
    data = dict()
    return JsonResponse(data)

def experiment_users_list(request, experiment_id):
    experiment = Experiments.objects.get(pk = experiment_id)
    users= experiment.users.values()
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/users_list.html', {'users': users,'experiment': experiment,'logged_user': logged_user})

def save_occupancies(sample, status):
    print("save_occupancies")
    layers = Layers.objects.filter(sample = sample)
    occupancies = []
    radiation_length_occupancy = 0
    nu_coll_length_occupancy = 0
    nu_int_length_occupancy = 0
    for layer in layers:
        compound_elements = CompoundElements.objects.filter(compound = layer.compound_type)
        if len(compound_elements) != 0:
            layer_radiation_length = 0 
            layer_nu_coll_length = 0
            layer_nu_int_length = 0
            for compound_element in compound_elements:
                layer_radiation_length = layer_radiation_length + compound_element.percentage * compound_element.element_type.radiation_length
                layer_nu_coll_length = layer_nu_coll_length + compound_element.percentage * compound_element.element_type.nu_coll_length
                layer_nu_int_length = layer_nu_int_length + compound_element.percentage * compound_element.element_type.nu_int_length
            layer_radiation_length = layer_radiation_length /100
            layer_nu_coll_length = layer_nu_coll_length / 100
            layer_nu_int_length = layer_nu_int_length / 100
            if layer.compound_type.density != 0:
                layer_linear_radiation_length = layer_radiation_length / layer.compound_type.density
                layer_linear_nu_coll_length = layer_nu_coll_length /  layer.compound_type.density
                layer_linear_nu_int_length = layer_nu_int_length / layer.compound_type.density
            else:
                layer_linear_radiation_length = 0
                layer_linear_nu_coll_length = 0
                layer_linear_nu_int_length = 0
            if layer_linear_radiation_length != 0: 
                radiation_length_occupancy = radiation_length_occupancy + layer.length /(10 * layer_linear_radiation_length)
            if layer_linear_nu_coll_length != 0:
                nu_coll_length_occupancy = nu_coll_length_occupancy + layer.length /(10 * layer_linear_nu_coll_length)
            if layer_linear_nu_int_length != 0:
                nu_int_length_occupancy = nu_int_length_occupancy + layer.length /(10 * layer_linear_nu_int_length)
    radiation_length_occupancy = radiation_length_occupancy * 100
    nu_coll_length_occupancy = nu_coll_length_occupancy * 100
    nu_int_length_occupancy = nu_int_length_occupancy * 100
    if status == "new" or status == "clone":
        sample_occupancy = Occupancies()
        sample_occupancy.sample = sample
    else:
        sample_occupancies =  Occupancies.objects.filter(sample = sample)
        if len(sample_occupancies) != 0:
            sample_occupancy = sample_occupancies[0]
        else:
            sample_occupancy = Occupancies()
            sample_occupancy.sample = sample
    sample_occupancy.radiation_length_occupancy = round(radiation_length_occupancy,3)
    sample_occupancy.nu_coll_length_occupancy = round(nu_coll_length_occupancy,3)
    sample_occupancy.nu_int_length_occupancy = round(nu_int_length_occupancy,3)     
    sample_occupancy.save()
    print("sample_occupancy")
    print(sample_occupancy)

def get_samples_occupancies(samples):
    samples_data = []
    for sample in samples:
        if sample.experiment.category == 'Passive Standard':
            sample_category = sample.category.split("standard",1)[1]
        else:
            sample_category = sample.category.split(":",1)[1]
        occupancy = Occupancies.objects.filter(sample=sample)
        if len(occupancy) == 0:
            save_occupancies(sample, "new")
        occupancy1 = Occupancies.objects.filter(sample=sample.id)[0]
        samples_data.append({
                "sample": sample,
                "sample_category": sample_category,
                "occupancy": occupancy1,
                })
    return samples_data

def archive_experiment_samples(request,experiment_id):
    logged_user = get_logged_user(request)
    experiment =  Experiments.objects.get(pk = experiment_id)
    archives = ArchiveExperimentSample.objects.filter(experiment = experiment)
    return render(request, 'samples_manager/archive_experiment_samples.html', {'archives': archives, 'logged_user':logged_user, 'experiment': experiment})

def move_samples(request, experiment_id):
    print("move samples")
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
                    print(new_archive)
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

def experiment_samples_list(request, experiment_id):
    print("experiment samples list")
    logged_user = get_logged_user(request)
    experiment = Experiments.objects.get(pk = experiment_id)
    samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
    samples_data = get_samples_occupancies(samples)
    irradiations = []
    experiments = authorised_experiments(logged_user)
    if  logged_user.role == 'Admin': 
        template_url = 'samples_manager/admin_samples_list.html'
    else:
         template_url = 'samples_manager/samples_list.html'
    return render(request,template_url, {'samples': samples,'samples_data': samples_data, 'experiment': experiment,'logged_user': logged_user, 'experiments':experiments})

def dosimeters_list(request):
    logged_user = get_logged_user(request)
    dosimeters = Dosimeters.objects.order_by('dos_id')
    return render(request, 'samples_manager/dosimeters_list.html', {'dosimeters': dosimeters, 'logged_user': logged_user})

def experiment_details(request, experiment_id):
    experiment = get_object_or_404(Experiments, pk=experiment_id)
    return render(request, 'samples_manager/experiment_details.html', {'experiment': experiment})


def user_details(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    return render(request, 'samples_manager/user_details.html', {'user': user})


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

#def generate_multiple_dos(request):




def generate_dos_id(dosimeter):
    if dosimeter.dos_id =='':
        all_dosimeters = Dosimeters.objects.all()
        dosimeters_numbers = []
        for dosimeter in all_dosimeters:
            if dosimeter.dos_id !='': 
                 dosimeters_numbers.append(int(dosimeter.dos_id[4:]))
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
                if val==assigned_dosimeters[idx-1]+1:
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
                    print ("sample saved")
                    if layers_formset.is_valid():
                        print("layers valid")
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
                    sample_temp = Samples.objects.create(**sample_data)
                    sample = Samples.objects.get(pk = sample_temp.pk)
                    sample.status = "Registered"
                    sample.created_by = logged_user
                    sample.updated_by = logged_user
                    sample.experiment = experiment
                    sample.save()
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
                                    print("saved layer")
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

def save_dosimeter_form(request,form1, form2, status, template_name):
    data = dict()
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        if form1.is_valid() and form2.is_valid():
            if status == 'new' or  status == 'clone':
                dosimeter_data = {}
                dosimeter_data.update(form1.cleaned_data)
                dosimeter_data.update(form2.cleaned_data)
                dosimeter_temp = Dosimeters.objects.create(**dosimeter_data)
                dosimeter = Dosimeters.objects.get(pk = dosimeter_temp.pk)
                dosimeter.status = "Registered"
                dosimeter.created_by = logged_user
                if dosimeter.dos_id =='':
                    print("generating")
                dosimeter.dos_id = generate_dos_id(dosimeter)
                dosimeter.save()
            elif status == 'update':
                dosimeter_updated = form1.save()
                form2.save()
                dosimeter_updated.status = "Updated"
                dosimeter_updated.updated_by = logged_user
                dosimeter_updated.save()
                print("sample updated")
            else:
                pass
            data['form_is_valid'] = True
            dosimeters = Dosimeters.objects.order_by('dos_id')
            data['html_dosimeter_list'] = render_to_string('samples_manager/partial_dosimeters_list.html', {
                'dosimeters':dosimeters
            })
        else:
            data['form_is_valid'] = False
    context = {'form1': form1, 'form2': form2}
    data['html_form'] = render_to_string(template_name, context, request=request)
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

def save_experiment_form_formset(request,form1, form2, form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, status, template_name):
    data = dict()
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        if status == 'new' or  status == 'clone': # status experiment
            if form1.is_valid() and form2.is_valid() and form3.is_valid() and fluence_formset.is_valid() and material_formset.is_valid():
                if form1.checking_unique() == True:
                    experiment_data = {}
                    experiment_data.update(form1.cleaned_data)
                    print(experiment_data)
                    experiment_data.update(form2.cleaned_data)
                    experiment_data.update(form3.cleaned_data)
                    experiment_temp = Experiments.objects.create(**experiment_data)
                    experiment = Experiments.objects.get(pk = experiment_temp.pk)
                    experiment.created_by =  logged_user 
                    experiment.updated_by =  logged_user
                    experiment.status = "Registered"
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
                        if fluence_formset.cleaned_data is not None:
                            for form in fluence_formset.forms:
                                fluence = form.save()
                                fluence.experiment = experiment
                                fluence.save()
                        else:
                            print("data none")
                    else:
                        print("fluence not valid")
                    if material_formset.is_valid():
                        if material_formset.cleaned_data is not None:
                            for form in material_formset.forms:
                                material= form.save()
                                material.experiment = experiment
                                material.save()
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
                    ##send_mail_notification( 'IRRAD Data Manager: New experiment registered in the CERN IRRAD Proton Irradiation Facility',message,'irrad.ps@cern.ch', experiment.responsible.email)
                    message2irrad=mark_safe("The user with the account: "+logged_user.email+" registered a new experiment with title: "+ experiment.title+".\nPlease, find all the registerd experiments in this link: https://irrad-data-manager.web.cern.ch/samples_manager/experiments/")
                    #send_mail_notification('IRRAD Data Manager: New experiment',message2irrad,logged_user.email,'irrad.ps@cern.ch')
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
                #send_mail_notification('IRRAD Data Manager: Updated experiment',message2irrad,logged_user.email,'irrad.ps@cern.ch')
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
                    print(fluence_formset.cleaned_data)
                    fluence_formset.save()
                    print(fluence_formset)
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
                #send_mail_notification('IRRAD Data Manager: Experiment  %s validation' % experiment.title,message,'irrad.ps@cern.ch',experiment.responsible.email)
                message2irrad='You validated the experiment with title: %s' % experiment.title
                #send_mail_notification('IRRAD Data Manager: Experiment %s validation' % experiment.title,message2irrad,'irrad.ps@cern.ch','irrad.ps@cern.ch')
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
                #send_mail_notification( 'IRRAD Data Manager: Experiment "%s"  was completed'%experiment.title,message,'irrad.ps@cern.ch', experiment.responsible.email)
                exp_users= updated_experiment.users.values()
                for user in exp_users:
                    pass
                    #send_mail_notification( 'IRRAD Data Manager: Experiment "%s"  was completed'%experiment.title,message,'irrad.ps@cern.ch', user['email'])
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

def irradiation_status_update(request, pk):
    data = dict()
    logged_user = get_logged_user(request)
    irradiation = get_object_or_404(Irradiation, pk=pk)
    if request.method == 'POST':
        form =  IrradiationStatus(request.POST,instance=irradiation)
        if form.is_valid():
            updated_irradiation =  form.save()
            data['form_is_valid'] = True
            irradiations = Irradiation.objects.all()
            template_data = {'irradiations': irradiations}
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
        #send_mail_notification( 'IRRAD Data Manager: Experiment "%s"  was deleted'%experiment.title,message,'irrad.ps@cern.ch', experiment.responsible.email)
        message2irrad=mark_safe("The user with the account: "+logged_user.email+" deleted the experiment with title '"+ experiment.title+"'.\n")
        #send_mail_notification( 'IRRAD Data Manager: Experiment "%s"  was deleted'%experiment.title,message2irrad,experiment.responsible.email, 'irrad.ps@cern.ch')
    else:
        context = {'experiment': experiment}
        data['html_form'] = render_to_string('samples_manager/partial_experiment_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

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
                print("here")
                message=mark_safe('Dear user,\nyou were assigned as a user for the experiment '+experiment.title+' by the account: '+logged_user.email+'.\nPlease, find all your experiments at this URL: http://cern.ch/irrad.data.manager/samples_manager/experiments/\nIn case you believe that this e-mail has been sent to you by mistake please contact us at irrad.ps@cern.ch.\nKind regards,\nCERN IRRAD team.\nhttps://ps-irrad.web.cern.ch')
                #send_mail_notification('IRRAD Data Manager: Registration to the experiment %s of CERN IRRAD Proton Irradiation Facility' %experiment.title,message,'irrad.ps@cern.ch', user.email)
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
    print(data)
    return JsonResponse(data)

def user_new(request,experiment_id):
    experiment = Experiments.objects.get(pk = experiment_id)
    if request.method == 'POST':
        form = UsersForm(request.POST)
    else:
        form = UsersForm()
    return save_user_form(request, form,experiment, 'samples_manager/partial_user_create.html')

def admin_user_new(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
    else:
        form = UsersForm()
    return save_admin_user_form(request, form, 'samples_manager/admin_partial_user_create.html')

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

def generate_dos_ids(request):
    data = dict()
    if request.method == 'POST':
        print("in request post")
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

def admin_user_update(request,pk):
    user = get_object_or_404(Users, pk = pk)
    if request.method == 'POST':
        form = UsersForm(request.POST, instance = user)
    else:
        form = UsersForm(instance = user)
    return save_admin_user_form(request, form,'samples_manager/admin_partial_user_update.html')

    
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


def dosimeter_new(request):
    logged_user = get_logged_user(request)
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

def print_experiment_view(request, pk):
    experiment = get_object_or_404(Experiments, pk=pk)
    filename="experiment %s.pdf" % experiment.title
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    Story = []
    style = styles["Normal"]
    #text = "Irradiation experiment title: %" +experiment.title+"\n Description:"+experiment.description+"\n CERN experiment Projects:"+experiment.description+"Constrains\n"+experiment.constraints)
    Story.append(Paragraph("Irradiation experiment title: %s" %experiment.title, style))
    Story.append(Spacer(1,0.2*inch))
    Story.append(Paragraph("Description: %s" %experiment.description, style))
    Story.append(Spacer(1,0.2*inch))
    Story.append(Paragraph("CERN experiments/Projects: %s" %experiment.cern_experiment, style))
    Story.append(Spacer(1,0.2*inch))
    Story.append(Paragraph("Responsible person: %s" %experiment.responsible, style))
    Story.append(Spacer(1,0.2*inch))
    Story.append(Paragraph("Availability: %s" %experiment.availability, style))
    Story.append(Spacer(1,0.2*inch))
    Story.append(Paragraph("Constraints: %s" %experiment.constraints, style))
    Story.append(Spacer(1,0.2*inch))
    Story.append(Paragraph("Number of Samples: %s" %experiment.number_samples, style))
    Story.append(Spacer(1,0.2*inch))
    Story.append(Paragraph("Category: %s" %experiment.category, style))
    Story.append(Spacer(1,0.2*inch))
    if experiment.category=="Passive Standard": # passive standard
        try:
            cat_instance  = PassiveStandardCategories.objects.get( experiment=experiment)
            text = "Irradiation area: "
            if cat_instance.irradiation_area_5x5: 
                text=text+mark_safe("5mmx5mm, ")
            if cat_instance.irradiation_area_10x10: 
                text=text+mark_safe("10mmx10mm, ")
            if cat_instance.irradiation_area_20x20:
                text=text+mark_safe("20mmx20mm ")
            Story.append(Paragraph(text, style))
            Story.append(Spacer(1,0.2*inch))
        except PassiveStandardCategories.DoesNotExist:
                print("no category found")
    elif experiment.category=="Passive Custom": # passive custom
        try:
            cat_instance  = PassiveCustomCategories.objects.get(experiment=experiment)
            Story.append(Paragraph("Type: %s" %cat_instance.passive_category_type, style))
            Story.append(Spacer(1,0.2*inch))
            Story.append(Paragraph("Irradiation area: %s" %cat_instance.passive_irradiation_area, style))
            Story.append(Spacer(1,0.2*inch))
            Story.append(Paragraph("Modus operandi: %s" %cat_instance.passive_modus_operandi, style))
            Story.append(Spacer(1,0.2*inch))
        except PassiveCustomCategories.DoesNotExist:
            print("no category found")
    if experiment.category=="Active": # active
        try:
            cat_instance  = ActiveCategories.objects.get( experiment=experiment)
            Story.append(Paragraph("Type: %s" %cat_instance.active_category_type, style))
            Story.append(Spacer(1,0.2*inch))
            Story.append(Paragraph("Irradiation area: %s" %cat_instance.active_irradiation_area, style))
            Story.append(Spacer(1,0.2*inch))
            Story.append(Paragraph("Modus operandi: %s" %cat_instance.active_modus_operandi, style))
            Story.append(Spacer(1,0.2*inch))
        except ActiveCategories.DoesNotExist:
            print("no category found")

    fluences = ReqFluences.objects.all().filter(experiment=experiment)
    fluences_text= "Requested fluences: "
    for fluence in fluences: 
        fluences_text= fluences_text + fluence.req_fluence+ ", "
    Story.append(Paragraph(fluences_text, style))
    Story.append(Spacer(1,0.2*inch))
    fluences = ReqFluences.objects.all().filter(experiment=experiment)

    materials = Materials.objects.all().filter(experiment=experiment)
    materials_text= "Types of samples: "
    for material in materials: 
        materials_text= materials_text + material.material+ " "
    Story.append(Paragraph(materials_text, style))
    Story.append(Spacer(1,0.2*inch))
    Story.append(Paragraph("Additional comments: %s" %experiment.comments, style))
    Story.append(Spacer(1,0.2*inch))
    doc.build(Story)
    fs = FileSystemStorage("")
    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"'%filename
        return response
    return response



def print_sample_view(request, experiment_id, pk):
    experiment = Experiments.objects.get(pk = experiment_id)
    sample = get_object_or_404(Samples, pk=pk)
    filename="sample %s.pdf" % sample.name
    user = Users.objects.get(email = experiment.responsible)
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    Story = []
    header_style = styles["Heading1"]
    header = "IRRAD Proton Facility Sample " +sample.set_id
    Story.append(Paragraph(header, header_style))
    Story.append(Spacer(1,0.3*inch))
    style = styles["Normal"]
    #text = "Irradiation experiment title: %" +experiment.title+"\n Description:"+experiment.description+"\n CERN experiment Projects:"+experiment.description+"Constrains\n"+experiment.constraints)
    sample_identification = "Sample details: "+ sample.material.material+" "+sample.name
    Story.append(Paragraph(sample_identification, style))
    Story.append(Spacer(1,0.1*inch))
    experiment_text = "Experiment: " +experiment.title+ " " +experiment.responsible.email+ " " + user.telephone
    Story.append(Paragraph(experiment_text, style))
    Story.append(Spacer(1,0.1*inch))
    dimensions_text = "Height: "+str(sample.height)+"mm Width: " +str(sample.width)+ "mm"
    Story.append(Paragraph(dimensions_text, style))
    Story.append(Spacer(1,0.1*inch))
    Story.append(Paragraph("Weight: %s kg" %sample.weight, style))
    Story.append(Spacer(1,0.1*inch))
    Story.append(Paragraph("Samples layers:", style))
    Story.append(Spacer(1,0.05*inch))
    layers = Layers.objects.all().filter(sample=sample)
    for layer in layers: 
        layer_text= "Name: "+layer.name+ " - Length: "+str(layer.length)+" mm  - Element name: "+str(layer.element_type)+ "  - Weight fraction: "+str(layer.percentage)+ "%  - Density: "+str(layer.density)+"  g/mL"
        Story.append(Paragraph(layer_text, style))
        Story.append(Spacer(1,0.05*inch))
    fluences = ReqFluences.objects.all().filter(experiment=experiment)
    Story.append(Paragraph("Requested fluence: %s protons/cm2" %sample.req_fluence.req_fluence, style))
    Story.append(Spacer(1,0.1*inch))
    Story.append(Paragraph("Category: %s" %sample.category, style))
    Story.append(Spacer(1,0.1*inch))
    Story.append(Paragraph("Storage: %s" %sample.storage, style))
    Story.append(Spacer(1,0.1*inch))
    Story.append(Paragraph("Location: %s" %sample.current_location, style))
    Story.append(Spacer(1,0.1*inch))
    Story.append(Paragraph("Comments: %s" %sample.comments, style))
    Story.append(Spacer(1,0.5*inch))

    data=[['SEC\nwanted', 'Time IN', 'Time OUT', 'SEC\nachieved', 'AL#','Fluence\nachieved','Comment'],
       ['Step\nReal SEC', 'DD/MM\nHH:MM', 'DD/MM\nHH:MM', 'Start\nStop', 'Nb.','p/cm2',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','',''],
       ['', '', '', '', '','','']]
    t=Table(data,7*[1.1*inch], 27*[0.5*inch])
    t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'CENTER'),
                       ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
                       ('BOX', (0,0), (-1,-1), 1, colors.black),
                       ]))
    Story.append(t)
    doc.build(Story)
    fs = FileSystemStorage("")
    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"'%filename
        return response
    return response


def print_sample_label_view(request, experiment_id, pk):
    data = dict()
    print("printing label!!!")
    experiment = Experiments.objects.get(pk = experiment_id)
    sample = get_object_or_404(Samples, pk=pk)
    if request.method == 'POST':
        sample.set_id = generate_set_id(sample)
        sample.save()
        data['set_id'] = sample.set_id
        data['req_fluence'] = sample.req_fluence.req_fluence
        category = sample.category
        print("data category")
        if experiment.category == 'Passive Standard':
            print(sample.category)
            data['category'] = sample.category.split("standard",1)[1]
        else:
            data['category'] = sample.category.split(":",1)[1]
        print('responsible')
        data['responsible'] = experiment.responsible.surname
        data['sample_name'] = sample.name
        samples = Samples.objects.filter(experiment = experiment).order_by('set_id')
        samples_data = get_samples_occupancies(samples)
        data['html_sample_list'] = render_to_string('samples_manager/partial_samples_list.html', {
                'samples': samples,
                'samples_data' : samples_data, 
                'experiment': experiment
            })
    else:
        context = {'sample': sample, 'experiment': experiment }
        data['html_form'] = render_to_string('samples_manager/partial_sample_print_label.html',
            context,
            request=request,
        )
    return JsonResponse(data)


def print_dosimeter_label_view(request, pk):
    data = dict()
    dosimeter = get_object_or_404(Dosimeters, pk=pk)
    if request.method == 'POST':
        data['dos_id'] = dosimeter.dos_id
        data['dos_type'] = dosimeter.dos_type
        dosimeters = Dosimeters.objects.all().order_by('dos_id')
        data['html_dosimeter_list'] = render_to_string('samples_manager/partial_dosimeters_list.html', {
                'dosimeters': dosimeters,
            })
    else:
        context = {'dosimeter': dosimeter}
        data['html_form'] = render_to_string('samples_manager/partial_dosimeter_print_label.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__contains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search_irradiations(request):
        query_string = ''
        found_entries = None
        irradiations =[]
        if ('search_box' in request.GET) and request.GET['search_box'].strip():
            query_string = request.GET['search_box']
            entry_query = get_query(query_string, ['status'])
            irradiations = Irradiation.objects.filter(entry_query)
        return render(request, 'samples_manager/irradiations_list.html', {'irradiations': irradiations})

def search_samples(request, experiment_id):
        query_string = ''
        found_entries = None
        samples = []
        logged_user = get_logged_user(request)
        experiment = Experiments.objects.get(pk = experiment_id)
        if ('search_box' in request.GET) and request.GET['search_box'].strip():
            query_string = request.GET['search_box']
            entry_query = get_query(query_string, ['set_id', 'name', 'category'])
            experiment_samples = Samples.objects.filter(experiment = experiment)
            samples = experiment_samples.filter(entry_query)
        return render(request, 'samples_manager/samples_list.html', {'samples': samples, 'logged_user':logged_user, 'experiment': experiment})


def search_experiments_user(request):
        query_string = ''
        found_entries = None
        samples = []
        logged_user = get_logged_user(request)
        if ('search_box' in request.GET) and request.GET['search_box'].strip():
            query_string = request.GET['search_box']
            entry_query = get_query(query_string, ['title', 'status', 'number_samples'])
            experiments = Experiments.objects.filter(entry_query)
            authorised_experiments = filtered_authorised_experiments(logged_user, experiments)
        return render(request, 'samples_manager/experiments_list.html', {'experiments': authorised_experiments, 'logged_user':logged_user})


def search_experiments_admin(request):
        query_string = ''
        found_entries = None
        samples = []
        logged_user = get_logged_user(request)
        if ('search_box' in request.GET) and request.GET['search_box'].strip():
            query_string = request.GET['search_box']
            entry_query = get_query(query_string, ['title', 'status'])
            experiments = Experiments.objects.filter(entry_query)
            experiment_data = get_registered_samples_number(experiments)
        return render(request, 'samples_manager/admin_experiments_list.html', {'experiment_data':experiment_data, 'logged_user': logged_user})

def search_experiment_users(request, experiment_id):
        query_string = ''
        found_entries = None
        samples = []
        logged_user = get_logged_user(request)
        experiment = Experiments.objects.get(pk = experiment_id)
        if ('search_box' in request.GET) and request.GET['search_box'].strip():
            query_string = request.GET['search_box']
            entry_query = get_query(query_string, ['email', 'name', 'surname', 'telephone', 'role'])
            experiment_users = experiment.users.values()
            users = experiment_users.filter(entry_query)
        return render(request, 'samples_manager/users_list.html', {'users': users, 'logged_user':logged_user, 'experiment': experiment})

def search_users_admin(request):
        query_string = ''
        found_entries = None
        samples = []
        logged_user = get_logged_user(request)
        if ('search_box' in request.GET) and request.GET['search_box'].strip():
            query_string = request.GET['search_box']
            entry_query = get_query(query_string, ['email', 'name', 'surname', 'telephone', 'role'])
            users = Users.objects.filter(entry_query)
        return render(request, 'samples_manager/admin_users_list.html', {'users': users, 'logged_user':logged_user})

def search_dosimeters(request):
        query_string = ''
        found_entries = None
        dosimeters = []
        logged_user = get_logged_user(request)
        if ('search_box' in request.GET) and request.GET['search_box'].strip():
            query_string = request.GET['search_box']
            entry_query = get_query(query_string, ['dos_id', 'height', 'width', 'status'])
            dosimeters = Dosimeters.objects.filter(entry_query)
        return render(request, 'samples_manager/dosimeters_list.html', {'dosimeters': dosimeters, 'logged_user':logged_user})


