from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Experiments,ReqFluences, Materials,PassiveStandardCategories,PassiveCustomCategories,ActiveCategories,Users
from django.template import loader
from django.core.urlresolvers import reverse
import datetime
from .forms import ExperimentsForm1,ExperimentsForm2,ExperimentsForm3, UsersForm, ReqFluencesForm, MaterialsForm, PassiveStandardCategoriesForm, PassiveCustomCategoriesForm,ActiveCategoriesForm
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



def send_mail_notification(title,message,from_mail,to_mail):
    '''headers = {'Reply-To': 'irrad.ps@cern.ch'}
    from_mail='irrad.ps@cern.ch'
    msg = EmailMessage(title,message,from_mail, to=[to_mail], headers = headers)
    msg.send()'''

def get_logged_user(request):
    #logged_user = request.META["HTTP_X_REMOTE_USER"]
    logged_user = 'blerina.gkotse@cern.ch'
    users = Users.objects.all()
    emails =[]
    for item in users:
        emails.append(item.email)
    if not logged_user in emails:
        new_user = Users()
        new_user.email = logged_user
        new_user.save()
    return logged_user
    

def index(request):
    template = loader.get_template('samples_manager/index.html')
    logged_user = get_logged_user(request)
    print(logged_user)
    context = {'logged_user': logged_user}
    return render(request, 'samples_manager/index.html', context)


def view_user(request):
    #only in production
    logged_user = get_logged_user(request)
    #logged_user = 'blerina.gkotse@cern.ch'
    html = "<html><body><div id='user_id'>User e-mail %s.</div></body></html>" %  logged_user
    return HttpResponse(html)

def regulations(request):
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/terms_conditions.html', {'logged_user': logged_user})

def all_experiments_list(request):
    #experiments = Experiments.objects.all().order_by('-updated_at')
    experiments = Experiments.objects.all()
    logged_user = get_logged_user(request)
    return render(request, 'samples_manager/registered_experiments_list.html', {'experiments': experiments,'logged_user': logged_user})

def experiments_list(request):
    #experiments = Experiments.objects.all().order_by('-updated_at')
    logged_user = get_logged_user(request)
    user = Users.objects.all().filter(email=logged_user)
    experiments = Experiments.objects.all().filter(responsible=user)
    return render(request, 'samples_manager/experiments_list.html', {'experiments': experiments, 'logged_user': logged_user})

def registered_experiments_list(request):
    experiments = Experiments.objects.all().filter(status="Registered")
    logged_user = get_logged_user(request)
    print(experiments)
    return render(request, 'samples_manager/registered_experiments_list.html', {'experiments': experiments,'logged_user': logged_user})
    
def users_list(request):
    users = Users.objects.all()
    return render(request, 'samples_manager/users_list.html', {'users': users,})


def experiment_details(request, experiment_id):
    experiment = get_object_or_404(Experiments, pk=experiment_id)
    return render(request, 'samples_manager/experiment_details.html', {'experiment': experiment})


def user_details(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    return render(request, 'samples_manager/user_details.html', {'user': user})

def save_sample_form(request,form, new, experiment_id, template_name):
    data = dict()
    print("in the save")
    logged_user = get_logged_user(request)
    if request.method == 'POST':
        print("post")
        if form.is_valid():
            print("form is valid")
            sample_temp = form.save()
            print("sample_temp")
            sample = Samples.objects.get(pk = sample_temp.pk)
            print(sample)
            if new == 0:
                print("new sample")
                sample.status = "Registered"
                user = Users.objects.get(email = logged_user)
                sample.created_by = user
                print("create by")
                '''sample.set_id = generate_set_id()'''
                print("set %s" %sample.set_id)
                sample.save()
                print ("saved")
            elif new == 1: 
                print("new == 1")
                sample.status = "Updated"
                user = Users.objects.get(email = logged_user)
                sample.update_by = user
                sample.save()
            elif new == 3:
                print("new == 3")
                sample.status = "Registered"
                user = Users.objects.get(email = logged_user)
                sample.created_by = user
                exp = Experiments.objects.get (pk = experiment_id)
                sample.experiment = exp
                '''set_id = generate_set_id()
                sample.set_id = set_id'''
                sample.save()
                print("saved")
            else:
                sample.save()
            print('getting all samples')
            data['form_is_valid'] = True
            samples = Samples.objects.all()
            print('html samples list')
            data['html_sample_list'] = render_to_string('samples_manager/partial_samples_list.html', {
                'samples':samples
            })
            data['experiment_id'] = experiment_id
        else:
            data['form_is_valid'] = False
            ##print("form errors %s" %form.errors)
    context = {'form': form}
    print("context")
    data['html_form'] = render_to_string(template_name, context, request=request)
    #print("html form")
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


def save_experiment_form_formset(request,form1, form2, form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, new, template_name):
    data = dict()
    logged_user = get_logged_user(request)
    user = Users.objects.get(email = logged_user)
    if request.method == 'POST':
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            if new == 0: # new experiment
                experiment_data = {}
                experiment_data.update(form1.cleaned_data)
                experiment_data.update(form2.cleaned_data)
                experiment_data.update(form3.cleaned_data)
                experiment_temp = Experiments.objects.create(**experiment_data)
                experiment = Experiments.objects.get(pk = experiment_temp.pk)
                experiment.created_by = user
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
                experiments = Experiments.objects.filter(responsible=user)
                data['form_is_valid'] = True
                data['html_experiment_list'] = render_to_string('samples_manager/partial_experiments_list.html', {
                        'experiments': experiments,
                    })
                data['state'] = "Created"
                message=mark_safe('Dear user,\nyour irradiation experiment with title: '+experiment.title+' was successfully registered by this account: '+logged_user+'.\nPlease, find all your experiments at this URL: http://cern.ch/irrad.data.manager/samples_manager/experiments/\nIn case you believe that this e-mail has been sent to you by mistake please contact us at irrad.ps@cern.ch.\nKind regards,\nIRRAD team.')
                send_mail_notification( 'New experiment registered in the IRRAD Proton Irradiation Facility',message,'irrad.ps@cern.ch', experiment.responsible.email)
                message2irrad=mark_safe("The user with the account: "+logged_user+" registered a new experiment with title: "+ experiment.title+".\nPlease, find all the registerd experiments in this link: http://cern.ch/irrad.data.manager/samples_manager/registered/experiments/")
                send_mail_notification('New experiment',message2irrad,logged_user,'irrad.ps@cern.ch')
            elif  new == 1:
                print("update")
                experiment_updated = form1.save()
                form2.save()
                form3.save()
                experiment = Experiments.objects.get(pk =  experiment_updated.pk)
                if experiment.status=='Validated':
                    experiment.status = "Updated"
                user = Users.objects.get(email = logged_user)
                experiment.update_by = user
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
                experiments = Experiments.objects.filter(responsible=user)
                data['html_experiment_list'] = render_to_string('samples_manager/partial_experiments_list.html', {
                        'experiments': experiments,
                    })
                data['state'] = "Updated"
                message2irrad=mark_safe("The user with e-mail: "+logged_user+" updated the experiment with title '"+experiment.title+"'.\nPlease, find all the experiments in this link: http://cern.ch/irrad.data.manager/samples_manager/experiments/all/")
                send_mail_notification('Updated experiment',message2irrad,logged_user,'irrad.ps@cern.ch')
            elif  new == 2:  # validation
                print("validation")
                experiment_updated = form1.save()
                form2.save()
                form3.save()
                experiment = Experiments.objects.get(pk =  experiment_updated.pk)
                experiment.status = "Validated"
                user = Users.objects.get(email = logged_user)
                experiment.update_by = user
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
                experiments = Experiments.objects.all()
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


def user_new(request):
    BoxesFormSet = inlineformset_factory( Users, Boxes,  fk_name='responsible', form=BoxesForm, extra=1)
    if request.method == 'POST':
        form = UsersForm(request.POST)
        fluence_formset = BoxesFormSet(request.POST)
    else:
        form = UsersForm()
        formset = BoxesFormSet()
    return save_user_form(request, form, formset, 'samples_manager/partial_user_create.html')

def experiment_new(request):
    logged_user = get_logged_user(request)
    user = Users.objects.get(email = logged_user)
    FluenceReqFormSet = inlineformset_factory( Experiments, ReqFluences, form=ReqFluencesForm, extra=1)
    MaterialReqFormSet = inlineformset_factory( Experiments, Materials, form=MaterialsForm, extra=1)
    cern_experiments = Experiments.objects.order_by().values('cern_experiment').distinct()
    cern_experiments_list = []
    for item in cern_experiments:
        cern_experiments_list.append(item['cern_experiment'])
    if request.method == 'POST':
        form1 = ExperimentsForm1(request.POST,data_list=cern_experiments_list)
        form2 = ExperimentsForm2(request.POST)
        form3 = ExperimentsForm3(request.POST)
        fluence_formset = FluenceReqFormSet(request.POST)
        material_formset = MaterialReqFormSet(request.POST)
        passive_standard_categories_form =  PassiveStandardCategoriesForm(request.POST)
        passive_custom_categories_form =  PassiveCustomCategoriesForm(request.POST)
        active_categories_form = ActiveCategoriesForm(request.POST)
    else:
        form1 = ExperimentsForm1(data_list=cern_experiments_list,initial={'responsible': user})
        form2 = ExperimentsForm2()
        form3 = ExperimentsForm3()
        fluence_formset = FluenceReqFormSet()
        material_formset = MaterialReqFormSet()
        passive_standard_categories_form =  PassiveStandardCategoriesForm()
        passive_custom_categories_form =  PassiveCustomCategoriesForm()
        active_categories_form = ActiveCategoriesForm()
    new = 0
    return save_experiment_form_formset(request, form1,form2,form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, new, 'samples_manager/partial_experiment_create.html')

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
    new = 1
    return save_experiment_form_formset(request, form1,form2,form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, new, 'samples_manager/partial_experiment_update.html')


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
    new = 2
    return save_experiment_form_formset(request, form1,form2,form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, new,'samples_manager/partial_experiment_validate.html')

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
    new = 0
    return save_experiment_form_formset(request, form1,form2,form3, fluence_formset, material_formset, passive_standard_categories_form, passive_custom_categories_form,active_categories_form, new, 'samples_manager/partial_experiment_clone.html')

def experiment_delete(request, pk):
    experiment = get_object_or_404(Experiments, pk=pk)
    data = dict()
    logged_user = get_logged_user(request)
    user = Users.objects.get(email = logged_user)
    if request.method == 'POST':
        experiment.delete()
        data['form_is_valid'] = True
        experiments = Experiments.objects.filter(responsible=user)
        message=mark_safe('Dear user,\nyour irradiation experiment with title '+experiment.title+' was deleted by the account: '+logged_user+'.\nPlease, find all your experiments at this URL: http://cern.ch/irrad.data.manager/samples_manager/experiments/\n\nKind regards,\nIRRAD team.')
        send_mail_notification( 'Experiment "%s"  was deleted'%experiment.title,message,'irrad.ps@cern.ch', experiment.responsible.email)
        message2irrad=mark_safe("The user with the account: "+logged_user+" deleted the experiment with title '"+ experiment.title+"'.\n")
        send_mail_notification( 'Experiment "%s"  was deleted'%experiment.title,message2irrad,experiment.responsible.email, 'irrad.ps@cern.ch')
        data['html_experiment_list'] = render_to_string('samples_manager/partial_experiments_list.html', {
            'experiments': experiments,
        })
        data['state']='Deleted'
    else:
        context = {'experiment': experiment}
        data['html_form'] = render_to_string('samples_manager/partial_experiment_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
    


def save_user_form(request,form,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            users = Users.objects.all()
            data['html_user_list'] = render_to_string('samples_manager/partial_users_list.html', {
                'users': users
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def user_new(request):
    BoxesFormSet = inlineformset_factory( Users, Boxes,  fk_name='responsible', form=BoxesForm, extra=1)
    if request.method == 'POST':
        form = UsersForm(request.POST)
        formset = BoxesFormSet(request.POST)
    else:
        form = UsersForm()
        formset = BoxesFormSet()
    return save_user_form(request, form,'samples_manager/partial_user_create.html')

def user_update(request, pk):
    user = get_object_or_404(Users, pk=pk)
    if request.method == 'POST':
        form = UsersForm(request.POST, instance=user)
    else:
        form = UsersForm(instance=user)
    return save_user_form(request, form, 'samples_manager/partial_user_update.html')

def user_delete(request, pk):
    user = get_object_or_404(Users, pk=pk)
    data = dict()
    if request.method == 'POST':
        user.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        users = Users.objects.all()
        data['html_user_list'] = render_to_string('samples_manager/partial_users_list.html', {
            'users': users
        })
    else:
        context = {'user': user}
        data['html_form'] = render_to_string('samples_manager/partial_user_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
    
def user_clone(request, pk):
        user = get_object_or_404(Users, pk=pk)
        if request.method == 'POST':
            form = UsersForm(request.POST, instance=user)
        else:
            form = UsersForm(instance=user)
        return save_user_form(request, form, 'samples_manager/partial_user_create.html')



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
