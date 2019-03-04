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
from django.db import connection
import re
from datetime import date
import random
import time
from django.utils.datastructures import MultiValueDictKeyError
import requests
from string import Template

def get_logged_user(request):
    username =  request.META["HTTP_X_REMOTE_USER"]
    firstname = request.META["HTTP_X_REMOTE_USER_FIRSTNAME"]
    lastname = request.META["HTTP_X_REMOTE_USER_LASTNAME"]
    telephone = request.META["HTTP_X_REMOTE_USER_PHONENUMBER"]
    email =  request.META["HTTP_X_REMOTE_USER_EMAIL"]
    mobile = request.META["HTTP_X_REMOTE_USER_MOBILENUMBER"]
    department = request.META["HTTP_X_REMOTE_USER_DEPARTMENT"] 
    home_institute = request.META["HTTP_X_REMOTE_USER_HOMEINSTITUTE"]

    """username =  "bgkotse"
    firstname =  "Ina"
    lastname = "Gkotse"
    telephone = "11111"
    #email =  "Blerina.Gkotse@telecom-bretagne.eu"
    email =  "Blerina.Gkotse@cern.ch"
    mobile = "12345"
    department = "EP/DT"
    home_institute = "MINES ParisTech"
    """

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
        logged_user = Users.objects.get(email = email)

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

def define_preferences(request):
    data = dict()
    logged_user = get_logged_user(request)
    try:
        userpreference = get_object_or_404(UserPreferences, user = logged_user)
        data['global_theme'] = userpreference.global_theme
        data['button_theme'] = userpreference.button_theme
        data['menu_theme'] = userpreference.menu_theme
        data['table_theme'] = userpreference.table_theme
    except:
        print("exception!")
        data['global_theme'] = ''
        data['button_theme'] = ''
        data['menu_theme'] = ''
        data['table_theme'] = ''
    return data

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

def send_mail_notification(title,message,from_mail,to_mail):
    '''headers = {'Reply-To': 'irrad.ps@cern.ch'}
    from_mail='irrad.ps@cern.ch'
    msg = EmailMessage(title,message,from_mail, to=[to_mail], headers = headers)
    msg.send()'''
    

def index(request):
    preference = define_preferences(request)
    template = loader.get_template('samples_manager/index.html')
    logged_user = get_logged_user(request)
    context = {'logged_user': logged_user,'prefered_theme':preference['global_theme'],'prefered_button':preference['button_theme'],'prefered_menu':preference['menu_theme'],'prefered_table':preference['table_theme']}
    return render(request, 'samples_manager/index.html', context)


def authorised_samples(logged_user):
    samples = []
    if logged_user.role == 'Admin':
        experiments = Experiments.objects.order_by('-updated_at')
    else:
         experiment_values = Experiments.objects.filter(Q(users=logged_user)|Q(responsible=logged_user)).values('title').distinct()
         experiments = []
         for value in experiment_values:
             experiment = Experiments.objects.get(title = value['title'])
             experiments.append(experiment)
    for experiment in experiments: 
        experiment_samples = Samples.objects.filter(experiment = experiment)
        for sample in experiment_samples:
            samples.append(sample)
    return samples

def regulations(request):
    preference = define_preferences(request)
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/terms_conditions.html', {'logged_user': logged_user,'prefered_theme':preference['global_theme'],'prefered_button':preference['button_theme'],'prefered_menu':preference['menu_theme'],'prefered_table':preference['table_theme']})

def fluence_conversion(request):
    preference = define_preferences(request)
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/fluence_conversion.html',{'logged_user': logged_user,'prefered_theme':preference['global_theme'],'prefered_button':preference['button_theme'],'prefered_menu':preference['menu_theme'],'prefered_table':preference['table_theme']})

def get_registered_samples_number(experiments):
    data = dict()
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

def register_preferences(request):
    global_theme = request.POST['global_theme']
    button_theme = request.POST['button']
    menu_theme = request.POST['segment']
    table_theme = request.POST['table']
    str_global_theme = str(global_theme)
    data = dict()
    if str_global_theme == '':
        data['form_is_valid'] = False
        print('data is not valid')
    else:
        data['form_is_valid'] = True
        logged_user = get_logged_user(request)
        try:
            userpreference = get_object_or_404(UserPreferences, user = logged_user)
            userpreference.global_theme =  global_theme
            userpreference.button_theme = button_theme
            userpreference.menu_theme = menu_theme
            userpreference.table_theme = table_theme
        except:
            userpreference = UserPreferences(global_theme = global_theme, button_theme = button_theme, menu_theme = menu_theme, table_theme = table_theme, user = logged_user)
        userpreference.save()
        data['global_theme'] = global_theme
        data['button_theme'] = button_theme
        data['menu_theme'] = menu_theme
        data['table_theme'] = table_theme
        print('save data')
    return JsonResponse(data)

def save_occupancies(sample, status):
    #print("save_occupancies")
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
    #print("sample_occupancy")
    #print(sample_occupancy)

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

def get_sample_fluences(sample):
    fluences = []
    irradiations = Irradiation.objects.filter(sample = sample)
    result = 0 
    tuple_list = []
    for irradiation in irradiations:
        if irradiation.accumulated_fluence:
            if '.' in str(irradiation.dosimeter):
                print('no calculation') 
            else:
                print('size:'+ str(irradiation.dosimeter.width)+ ' x '+ str(irradiation.dosimeter.height))
                dosimeter_area =  irradiation.dosimeter.width * irradiation.dosimeter.height
                dos_position = irradiation.dos_position
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
    return fluences
    


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
                    dosimeter.dos_id = generate_dos_id(dosimeter)
                dosimeter.save()
            elif status == 'update':
                dosimeter_updated = form1.save()
                form2.save()
                dosimeter_updated.status = "Updated"
                dosimeter_updated.updated_by = logged_user
                dosimeter_updated.save()
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
        layer_text= "Name: "+layer.name+ " - Length: "+str(layer.length)+" mm  - Element/Compound: "+str(layer.compound_type.name)
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
        return render(request, 'samples_manager/samples_list.html', {'samples': samples,  'experiment': experiment})


def select_table(request):
        logged_user = get_logged_user(request)
        tables = ['IRRAD1','IRRAD3','IRRAD5','IRRAD7','IRRAD9','IRRAD11','IRRAD13','IRRAD15','IRRAD17','IRRAD19']
        query_string = ''
        found_entries = None
        irradiations =[]
        if ('irrad_table' in request.GET) and request.GET['irrad_table'].strip():
            query_string = request.GET['irrad_table']
            entry_query = get_query(query_string, ['irrad_table'])
            irradiations = Irradiation.objects.filter(entry_query)
        return render(request, 'samples_manager/irradiations_list.html', {'irradiations': irradiations, 'logged_user':logged_user, 'tables':tables})


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


def get_sec(request):
    irradiations = Irradiation.objects.filter(~Q(status = 'Completed'))
    cursor = connection.cursor()
    data = dict()
    in_beam_checked = 0
    for irradiation in irradiations: 
        if irradiation.in_beam is True:
            in_beam_checked = in_beam_checked + 1         
            date_in = irradiation.date_in.astimezone(pytz.timezone("Europe/Paris"))
            timestamp = date_in.strftime('%Y-%m-%d %H:%M:%S')
            print("date in: ",timestamp)
            cursor.execute("SELECT SEC_VALUE FROM SEC_DATA WHERE SEC_ID = 'SEC_01' AND TIMESTAMP>TO_DATE('"+str(timestamp)+"', 'YYYY-MM-DD HH24:MI:SS')")
            rows=cursor.fetchall()
            sec_sum = 0
            for row in rows:
                sec_sum = sec_sum + row[0]
            irradiation.sec = sec_sum
            irradiation.save()
    data['form_is_valid'] = True
    data['in_beam_checked'] = in_beam_checked
    data['html_irradiation_list'] = render_to_string('samples_manager/partial_irradiations_list.html',{'irradiations': irradiations},request=request)
    return JsonResponse(data)

def in_beam_change(request):
    checked_irradiations = request.POST.getlist('in_beam_checkbox[]')
    checked_irradiation_ids = []
    irradiations = Irradiation.objects.filter(~Q(status = 'Completed'))
    in_beam_checked = 0
    for checked_irradiation in checked_irradiations:
        irradiation_splitted =  checked_irradiation.split("-")
        irradiation_id = irradiation_splitted[0]
        checked_irradiation_ids.append(irradiation_id)
        in_beam_checked = in_beam_checked + 1 
    print(checked_irradiation_ids)
    for irradiation in irradiations:
        if str(irradiation.id) in checked_irradiation_ids:
            irradiation.in_beam = True
            print(irradiation.in_beam)
        else:
            irradiation.in_beam = False
        irradiation.save()
    data = dict()
    print("irradiations saved")
    data['form_is_valid'] = True
    data['in_beam_checked'] = in_beam_checked
    #new_irradiations = Irradiation.objects.filter(~Q(status = 'Completed'))
    new_irradiations = Irradiation.objects.all()
    data['html_irradiation_list'] = render_to_string('samples_manager/partial_irradiations_list.html',{'irradiations': new_irradiations},request=request)
    return JsonResponse(data)

def webservice_test(request):
    url = "http://cmmsx-test.cern.ch/WSHub/SOAP"
    body="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsh="http://cern.ch/cmms/infor/wshub">
    <soapenv:Header/>
    <soapenv:Body>
        <wsh:readEquipment>
            <equipmentCode>PXXISET001-CR002706</equipmentCode>
            <credentials>
                <password>Maurice009</password>
                <username>irrad</username>
            </credentials>
            <sessionID></sessionID>
        </wsh:readEquipment>
    </soapenv:Body>
    </soapenv:Envelope>"""
    headers = { 
                "Host": "cmmsx-test.cern.ch",
                "Accept-Encoding": "gzip,deflate",
                "Content-Type": "text/xml;charset=UTF-8",
                "SOAPAction": "",
                "Content-Length": "657",
                "Host": "cmmsx-test.cern.ch",
                "Connection": "Keep-Alive",
                "User-Agent": "Apache-HttpClient/4.1.1 (java 1.5)",
}
    response = requests.post(url,data=body,headers=headers)
    print(response)
    data = {}
    return JsonResponse(data)











