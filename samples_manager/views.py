from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Experiments,ReqFluences, Materials,PassiveStandardCategories,PassiveCustomCategories,ActiveCategories,Users,Samples
from django.template import loader
from django.core.urlresolvers import reverse
import datetime
from .forms import ExperimentsForm1,ExperimentsForm2,ExperimentsForm3, UsersForm, ReqFluencesForm, MaterialsForm, PassiveStandardCategoriesForm, PassiveCustomCategoriesForm,ActiveCategoriesForm, SamplesForm1, SamplesForm2 
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.utils.safestring import mark_safe
import logging 



def send_mail_notification(title,message,from_mail,to_mail):
    '''headers = {'Reply-To': 'irrad.ps@cern.ch'}
    from_mail='irrad.ps@cern.ch'
    msg = EmailMessage(title,message,from_mail, to=[to_mail], headers = headers)
    msg.send()'''

def get_logged_user(request):
    '''username =  request.META["HTTP_X_REMOTE_USER"]
    firstname = request.META["HTTP_X_REMOTE_USER_FIRSTNAME"]
    lastname = request.META["HTTP_X_REMOTE_USER_LASTNAME"]
    email =  request.META["HTTP_X_REMOTE_USER_EMAIL"]'''
    firstname = 'Blerina'
    lastname = 'Gkotse'
    email = 'blerina.gkotse@cern.ch'
    users = Users.objects.all()
    emails =[]

    for item in users:
        emails.append(item.email)
    if not email in emails:
        new_user = Users()
        if firstname is not None:
            new_user.name= firstname
        if lastname is not None:
            new_user.surname = lastname
        if email is not None:
            new_user.email = email
        new_user.save()
        logged_user =  new_user
    else:
        logged_user = Users.objects.get( email = email)
    return logged_user
    

def index(request):
    template = loader.get_template('samples_manager/index.html')
    logged_user = get_logged_user(request)
    print(logged_user)
    context = {'logged_user': logged_user.email}
    return render(request, 'samples_manager/index.html', context)


def view_user(request):
    #only in production
    logged_user = get_logged_user(request)
    #logged_user = 'blerina.gkotse@cern.ch'
    html = "<html><body><div id='user_id'>User e-mail %s.</div></body></html>" %  logged_user.email
    return HttpResponse(html)

def regulations(request):
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/terms_conditions.html', {'logged_user': logged_user.email})

def all_experiments_list(request):
    experiments = Experiments.objects.order_by('-updated_at')
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/registered_experiments_list.html', {'experiments': experiments,'logged_user': logged_user.email})

def experiments_list(request):
    logged_user = get_logged_user(request)
    if logged_user.role == 'Admin':
        experiments = Experiments.objects.order_by('-updated_at')
        logged_user = get_logged_user(request)
        return render(request, 'samples_manager/registered_experiments_list.html', {'experiments': experiments,'logged_user': logged_user.email})
    else:
        experiments = Experiments.objects.all().filter(responsible=logged_user).order_by('-updated_at')
        return render(request, 'samples_manager/experiments_list.html', {'experiments': experiments, 'logged_user': logged_user.email})

def registered_experiments_list(request):
    experiments = Experiments.objects.all().filter(status="Registered").order_by('-updated_at')
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/registered_experiments_list.html', {'experiments': experiments,'logged_user': logged_user.email})
    
def users_list(request):
    users = Users.objects.all()
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/users_list.html', {'users': users,'logged_user': logged_user.email})

def experiment_users_list(request, experiment_id):
    experiment = Experiments.objects.get(pk = experiment_id)
    users= experiment.users.values()
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/users_list.html', {'users': users,'experiment': experiment,'logged_user': logged_user.email})


def experiment_samples_list(request, experiment_id):
    logged_user = get_logged_user(request)
    experiment = Experiments.objects.get(pk = experiment_id)
    samples = Samples.objects.filter(experiment = experiment).order_by('-updated_at')
    return render(request, 'samples_manager/samples_list.html', {'samples': samples, 'experiment': experiment,'logged_user': logged_user.email })


def experiment_details(request, experiment_id):
    experiment = get_object_or_404(Experiments, pk=experiment_id)
    return render(request, 'samples_manager/experiment_details.html', {'experiment': experiment})


def user_details(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    return render(request, 'samples_manager/user_details.html', {'user': user})
    
def save_sample_form(request,form1,form2, status, experiment, template_name):
    data = dict()
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        print("post")
        if form1.is_valid() and form2.is_valid():
            if status == 'new':
                print("status")
                sample_data = {}
                sample_data.update(form1.cleaned_data)
                sample_data.update(form2.cleaned_data)
                sample_temp = Samples.objects.create(**sample_data)
                sample = Samples.objects.get(pk = sample_temp.pk)
                sample.status = "Registered"
                sample.created_by = logged_user
                sample.experiment = experiment
                '''sample.set_id = generate_set_id()'''
                sample.save()
                print ("saved")
            elif status == 'update': 
                sample_updated = form1.save()
                form2.save()
                sample_updated.status = "Updated"
                sample_updated.update_by = logged_user
                sample_updated.save()
            else:
                sample_updated = form1.save()
                form2.save()
                sample_updated.save()
            data['form_is_valid'] = True
            samples = Samples.objects.filter(experiment = experiment).order_by('-updated_at')
            data['html_sample_list'] = render_to_string('samples_manager/partial_samples_list.html', {
                'samples':samples,
                'experiment': experiment
            })
        else:
            data['form_is_valid'] = False
            logging.warning('Sample data invalid')
    context = {'form1': form1,'form2': form2, 'experiment':experiment}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def save_dosimeter_form(request,form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            dosimeters = Dosimeters.objects.all()
            data['html_dosimeter_list'] = render_to_string('samples_manager/partial_dosimeters_list.html', {
                'dosimeters':dosimeters
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def save_experiment_form_formset(request,form1, form2, form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, status, template_name):
    data = dict()
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            if status == 'new' or  status == 'clone': # status experiment
                experiment_data = {}
                experiment_data.update(form1.cleaned_data)
                experiment_data.update(form2.cleaned_data)
                experiment_data.update(form3.cleaned_data)
                #users=experiment_data.pop('users')
                logging.warning(experiment_data)
                experiment_temp = Experiments.objects.create(**experiment_data)
                experiment = Experiments.objects.get(pk = experiment_temp.pk)
                experiment.created_by =  logged_user 
                experiment.status = "Registered"
                experiment.save()
                logging.warning('Experiment saved')
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
                    print( fluence_formset)
                    if fluence_formset.cleaned_data is not None:
                        for form in fluence_formset.forms:
                            fluence = form.save()
                            fluence.experiment = experiment
                            fluence.save()
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
                    output_template = 'samples_manager/partial_registered_experiments_list.html'
                else: 
                    experiments = Experiments.objects.filter(responsible = logged_user ).order_by('-updated_at')
                    output_template = 'samples_manager/partial_experiments_list.html'
                data['html_experiment_list'] = render_to_string(output_template, {
                        'experiments': experiments,
                        })
                data['state'] = "Created"
                message=mark_safe('Dear user,\nyour irradiation experiment with title: '+experiment.title+' was successfully registered by this account: '+logged_user.email+'.\nPlease, find all your experiments at this URL: http://cern.ch/irrad.data.manager/samples_manager/experiments/\nIn case you believe that this e-mail has been sent to you by mistake please contact us at irrad.ps@cern.ch.\nKind regards,\nIRRAD team.')
                send_mail_notification( 'New experiment registered in the IRRAD Proton Irradiation Facility',message,'irrad.ps@cern.ch', experiment.responsible.email)
                message2irrad=mark_safe("The user with the account: "+logged_user.email+" registered a new experiment with title: "+ experiment.title+".\nPlease, find all the registerd experiments in this link: http://cern.ch/irrad.data.manager/samples_manager/registered/experiments/")
                send_mail_notification('New experiment',message2irrad,logged_user.email,'irrad.ps@cern.ch')
            elif  status == 'update':
                print("update")
                experiment_updated = form1.save()
                form2.save()
                form3.save()
                experiment = Experiments.objects.get(pk =  experiment_updated.pk)
                if experiment.status=='Validated':
                    experiment.status = "Updated"
                experiment.update_by = logged_user
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
                if  material_formset.is_valid():    
                    material_formset.save()
                data['form_is_valid'] = True
                if logged_user.role == 'Admin':
                    experiments = Experiments.objects.all()
                    output_template = 'samples_manager/partial_registered_experiments_list.html'
                else: 
                    experiments = Experiments.objects.filter(responsible = logged_user ).order_by('-updated_at')
                    output_template = 'samples_manager/partial_experiments_list.html'
                data['html_experiment_list'] = render_to_string(output_template, {
                        'experiments': experiments,
                        })
                data['state'] = "Updated"
                message2irrad=mark_safe("The user with e-mail: "+logged_user.email+" updated the experiment with title '"+experiment.title+"'.\nPlease, find all the experiments in this link: http://cern.ch/irrad.data.manager/samples_manager/experiments/all/")
                send_mail_notification('Updated experiment',message2irrad,logged_user.email,'irrad.ps@cern.ch')
            elif  status == 'validate':  # validation
                print("validation")
                experiment_updated = form1.save()
                form2.save()
                form3.save()
                experiment = Experiments.objects.get(pk =  experiment_updated.pk)
                experiment.status = "Validated"
                experiment.update_by = logged_user
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
                if  material_formset.is_valid():    
                    material_formset.save()
                data['form_is_valid'] = True
                experiments = Experiments.objects.all().order_by('-updated_at')
                data['state'] = "Validated"
                data['html_experiment_list'] = render_to_string('samples_manager/partial_registered_experiments_list.html', {
                            'experiments': experiments,
                        })
                message='Your experiment with title "%s" was validated. \n Please, find all your experiments in this link: https://irrad-data-manager.web.cern.ch/samples_manager/experiments/'% experiment.title
                send_mail_notification('Experiment: %s validation' % experiment.title,message,'irrad.ps@cern.ch',experiment.responsible.email)
                message2irrad='You validated the experiment with title: %s' % experiment.title
                send_mail_notification('Experiment: %s validation' % experiment.title,message2irrad,'irrad.ps@cern.ch','irrad.ps@cern.ch')
                print("Message sent")
            else:
                 print("nothing to do")
        else:
            data['form_is_valid'] = False
            print("not valid")
    context = {'form1': form1,'form2': form2, 'form3': form3, 'fluence_formset': fluence_formset, 'material_formset': material_formset, 'passive_standard_categories_form': passive_standard_categories_form, 'passive_custom_categories_form': passive_custom_categories_form, 'active_categories_form': active_categories_form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    print("all saved!")
    return JsonResponse(data)

def experiment_new(request):
    logged_user = get_logged_user(request)
    FluenceReqFormSet = inlineformset_factory( Experiments, ReqFluences, form=ReqFluencesForm, extra=1)
    MaterialReqFormSet = inlineformset_factory( Experiments, Materials, form=MaterialsForm, extra=1)
    cern_experiments = Experiments.objects.order_by().values('cern_experiment').distinct()
    cern_experiments_list = []
    for item in cern_experiments:
        cern_experiments_list.append(item['cern_experiment'])
    if request.method == 'POST':
        print("in the post!")
        logging.warning('POST request')
        form1 = ExperimentsForm1(request.POST,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(request.POST)
        form3 = ExperimentsForm3(request.POST)
        fluence_formset = FluenceReqFormSet(request.POST)
        material_formset = MaterialReqFormSet(request.POST)
        passive_standard_categories_form =  PassiveStandardCategoriesForm(request.POST)
        passive_custom_categories_form =  PassiveCustomCategoriesForm(request.POST)
        active_categories_form = ActiveCategoriesForm(request.POST)
    else:
        form1 = ExperimentsForm1(data_list=cern_experiments_list,)
        form2 = ExperimentsForm2()
        form3 = ExperimentsForm3()
        fluence_formset = FluenceReqFormSet()
        material_formset = MaterialReqFormSet()
        passive_standard_categories_form =  PassiveStandardCategoriesForm()
        passive_custom_categories_form =  PassiveCustomCategoriesForm()
        active_categories_form = ActiveCategoriesForm()
    status = 'new'
    return save_experiment_form_formset(request, form1,form2,form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, status, 'samples_manager/partial_experiment_create.html')

def experiment_update(request, pk):
    cern_experiments = Experiments.objects.order_by().values('cern_experiment').distinct()
    cern_experiments_list = []
    for item in cern_experiments:
        cern_experiments_list.append(item['cern_experiment'])
    experiment = get_object_or_404(Experiments, pk=pk)
    FluenceReqFormSet = inlineformset_factory( Experiments, ReqFluences, form=ReqFluencesForm, extra=1)
    MaterialFormSet = inlineformset_factory( Experiments, Materials, form=MaterialsForm, extra=1)
    if request.method == 'POST':
        form1 = ExperimentsForm1(request.POST, instance=experiment,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(request.POST, instance=experiment)
        form3 = ExperimentsForm3(request.POST, instance=experiment)
        fluence_formset = FluenceReqFormSet(request.POST, instance=experiment)
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
        fluence_formset = FluenceReqFormSet(instance=experiment)
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
    FluenceReqFormSet = inlineformset_factory( Experiments, ReqFluences, form=ReqFluencesForm, extra=1)
    MaterialFormSet = inlineformset_factory( Experiments, Materials, form=MaterialsForm, extra=1)
    if request.method == 'POST':
        form1 = ExperimentsForm1(request.POST, instance=experiment,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(request.POST, instance=experiment)
        form3 = ExperimentsForm3(request.POST, instance=experiment)
        fluence_formset = FluenceReqFormSet(request.POST, instance=experiment)
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
        fluence_formset = FluenceReqFormSet(instance=experiment)
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
    FluenceReqFormSet = inlineformset_factory( Experiments, ReqFluences, form=ReqFluencesForm, extra=1)
    MaterialFormSet = inlineformset_factory( Experiments, Materials, form=MaterialsForm, extra=1)
    if request.method == 'POST':
        form1 = ExperimentsForm1(request.POST, instance=experiment,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(request.POST, instance=experiment)
        form3 = ExperimentsForm3(request.POST, instance=experiment)
        fluence_formset = FluenceReqFormSet(request.POST)
        material_formset = MaterialFormSet(request.POST)
        passive_standard_categories_form = PassiveStandardCategoriesForm(request.POST)
        passive_custom_categories_form = PassiveCustomCategoriesForm(request.POST)
        active_categories_form = ActiveCategoriesForm(request.POST)
    else:
        form1 = ExperimentsForm1(instance=experiment,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(instance=experiment)
        form3 = ExperimentsForm3(instance=experiment)
        fluence_formset = FluenceReqFormSet()
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
                experiments = Experiments.objects.all()
                output_template = 'samples_manager/partial_registered_experiments_list.html'
        else: 
                experiments = Experiments.objects.filter(responsible = logged_user ).order_by('-updated_at')
                output_template = 'samples_manager/partial_experiments_list.html'
        data['html_experiment_list'] = render_to_string(output_template, {
                'experiments': experiments,
        })
        data['state']='Deleted'
        message=mark_safe('Dear user,\nyour irradiation experiment with title '+experiment.title+' was deleted by the account: '+logged_user.email+'.\nPlease, find all your experiments at this URL: http://cern.ch/irrad.data.manager/samples_manager/experiments/\n\nKind regards,\nIRRAD team.')
        send_mail_notification( 'Experiment "%s"  was deleted'%experiment.title,message,'irrad.ps@cern.ch', experiment.responsible.email)
        message2irrad=mark_safe("The user with the account: "+logged_user.email+" deleted the experiment with title '"+ experiment.title+"'.\n")
        send_mail_notification( 'Experiment "%s"  was deleted'%experiment.title,message2irrad,experiment.responsible.email, 'irrad.ps@cern.ch')
    else:
        context = {'experiment': experiment}
        data['html_form'] = render_to_string('samples_manager/partial_experiment_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
    


def save_user_form(request, form, experiment, template_name):
    data = dict()
    if request.method == 'POST':
        logging.warning("post")
        if form.is_valid():
            logging.warning("form is valid")
            print(form.cleaned_data)
            new_user = form.save()
            print(new_user)
            experiment.users.add(new_user)
            print(new_user)
            data['form_is_valid'] = True
            users = experiment.users.all()
            data['html_user_list'] = render_to_string('samples_manager/partial_users_list.html', {
                'users': users,
                'experiment':experiment
            })
            print('done')
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'experiment': experiment}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


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

def user_delete(request,experiment_id,pk):
    experiment = Experiments.objects.get(pk = experiment_id)
    user = get_object_or_404(Users, pk=pk)
    data = dict()
    print(experiment)
    if request.method == 'POST':
        user.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        users = experiment.users.all()
        data['html_user_list'] = render_to_string('samples_manager/partial_users_list.html', {
            'users': users,
            'experiment':experiment
        })
    else:
        context = {'user': user, 'experiment':experiment,}
        data['html_form'] = render_to_string('samples_manager/partial_user_delete.html',
            context,
            request=request,
        )
        print(data['html_form'])
    return JsonResponse(data)
    
def sample_new(request, experiment_id):
    experiment = Experiments.objects.get(pk = experiment_id)
    print(experiment)
    if request.method == 'POST':
        form1 = SamplesForm1(request.POST, experiment_id = experiment.id)
        form2 = SamplesForm2(request.POST, experiment_id = experiment.id)
    else:
        form1 = SamplesForm1(experiment_id = experiment.id)
        form2 = SamplesForm2(experiment_id = experiment.id)
    status = 'new'
    return save_sample_form(request,form1, form2,status,experiment,'samples_manager/partial_sample_create.html')


def sample_update(request, experiment_id, pk):
    experiment = Experiments.objects.get(pk = experiment_id)
    sample = get_object_or_404(Samples, pk=pk)
    if request.method == 'POST':
        form1 = SamplesForm1(request.POST, instance=sample, experiment_id = experiment.id)
        form2 = SamplesForm2(request.POST, instance=sample, experiment_id = experiment.id)
    else:
        form1 = SamplesForm1(instance=sample, experiment_id = experiment.id)
        form2 = SamplesForm2(instance=sample, experiment_id = experiment.id)
    status = 'update'
    return save_sample_form(request,form1,form2, status,experiment, 'samples_manager/partial_sample_update.html')


def sample_clone(request, experiment_id, pk):
    experiment = Experiments.objects.get(pk = experiment_id)
    sample = get_object_or_404(Samples, pk=pk)
    if request.method == 'POST':
        form1 = SamplesForm1(request.POST, experiment_id = experiment.id)
        form2 = SamplesForm2(request.POST, experiment_id = experiment.id)
    else:
        form1 = SamplesForm1(experiment_id = experiment.id, instance=sample)
        form2 = SamplesForm2(experiment_id = experiment.id, instance=sample)
    status = 'clone'
    return save_sample_form(request, form1,form2, status, experiment, 'samples_manager/partial_sample_create.html')

def sample_delete(request,experiment_id, pk):
    print("in delete")
    experiment = Experiments.objects.get(pk = experiment_id)
    sample = get_object_or_404(Samples, pk=pk)
    data = dict()
    if request.method == 'POST':
        sample.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        samples = Samples.objects.filter(experiment = experiment).order_by('-updated_at')
        data['html_sample_list'] = render_to_string('samples_manager/partial_samples_list.html', {
            'samples': samples
        })
    else:
        context = {'sample': sample, 'experiment': experiment }
        data['html_form'] = render_to_string('samples_manager/partial_sample_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def print_experiment_view(request, pk):
    print("printing")
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
    Story.append(Paragraph("CERN experiments/Projects: %s" %experiment.description, style))
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
