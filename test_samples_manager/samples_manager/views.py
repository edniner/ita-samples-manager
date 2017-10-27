from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Experiments, Samples
from django.template import loader
from django.core.urlresolvers import reverse
import datetime
from .forms import ExperimentsForm, SamplesForm, UsersForm

def index(request):
    latest_Experiments_list = Experiments.objects.order_by('-id')[:15]
    latest_Samples_list = Samples.objects.order_by('-id')[:15]
    template = loader.get_template('samples_manager/index.html')
    context = {
        'latest_Experiments_list': latest_Experiments_list,
        'latest_Samples_list': latest_Samples_list,
    }
    return render(request, 'samples_manager/index.html', context)

def experiment_details(request, experiment_id):
    experiment = get_object_or_404(Experiments, pk=experiment_id)
    return render(request, 'samples_manager/experiment_details.html', {'experiment': experiment})

def sample_details(request, sample_id):
    sample = get_object_or_404(Samples, pk=sample_id)
    return render(request, 'samples_manager/sample/sample_details.html', {'sample': sample})

def experiment_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ExperimentsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:)
            form.save()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ExperimentsForm()
    return render(request, 'samples_manager/new_experiment.html', {'form': form})

def sample_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SamplesForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:)
            form.save()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SamplesForm()
    return render(request, 'samples_manager/new_sample.html', {'form': form})

def user_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UsersForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:)
            form.save()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UsersForm()
    return render(request, 'samples_manager/new_user.html', {'form': form})


def thankyou(request):
    return HttpResponse("Thank you!")

'''def new_experiment_submit(request):
    #new_experiment=Experiments.objects.create(id=7,title="test7", max_requested_fluence="1E10", start_date=datetime.datetime.now(), end_date=datetime.datetime.now(),planning="",resources="",storage="",experiment_type="",category="",regulations_flag=1,comments="")
    new_experiment=Experiments(id=8,title=request.POST['experiment_title'],max_requested_fluence=request.POST['max_requested_fluence'],start_date=request.POST['start_date'],end_date=request.POST['end_date'],planning=request.POST['experiment_planning'],resources=request.POST['resources'],storage=request.POST['storage'],experiment_type=request.POST['experiment_type'],category=request.POST['category'],regulations_flag=request.POST.get('general_regulations', False),comments=request.POST['justification'])
    new_experiment.save()
    return HttpResponseRedirect(reverse('samples_manager:title',args=(1,)))'''


