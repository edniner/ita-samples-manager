from django import forms
from django.contrib.admin import widgets   
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm,DateTimeInput,Textarea
from .models import Experiments, Samples, Users


class ExperimentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperimentsForm, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False
        self.fields['justification'].required = False
        self.fields['planning'].required = False
        self.fields['storage'].required = False
        self.fields['resources'].required = False
        self.fields['title'].label='Irradiation title'
        self.fields['start_date'].label= 'When the samples will be available for irradiation (if any)'
        self.fields['end_date'].label= 'Deadline for the end of irradiation (if any)'
        self.fields['justification'].label='Justification for the deadline (if any)'
        self.fields['category'].label='Choose category of irradiation'
        self.fields['resources'].label='Requested space/ resources'


    class Meta:
        model = Experiments
        fields = ['title', 'max_requested_fluence', 'start_date','end_date','justification','irradiation_type','category','planning','resources','storage','regulations_flag']
        widgets = {
            'start_date': DateTimeInput,
            'end_date': DateTimeInput,
            'planning': forms.Textarea(attrs={'rows':3}),
            'resources': forms.Textarea(attrs={'rows':3}),
            'justification': forms.Textarea(attrs={'rows':3}),
        }

class SamplesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SamplesForm, self).__init__(*args, **kwargs)
        self.fields['weight'].required = False
        self.fields['comments'].required = False
        self.fields['description'].label= 'Name/Description'
        self.fields['cern_experiment'].label= 'CERN experiment'



    class Meta:
        model = Samples
        fields = ['description', 'size', 'weight','material','requested_fluence','cern_experiment','comments','experiment_id']
        widgets = {
            'comments': forms.Textarea(attrs={'rows':3}),
        }


class UsersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Users
        fields = ['name', 'surname', 'email','telephone']
        widgets = { 
        }






