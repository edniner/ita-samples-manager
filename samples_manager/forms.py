# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets   
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm,DateTimeInput,Textarea
from .models import Experiments,Users, ReqFluences,Materials, PassiveStandardCategories,PassiveCustomCategories,ActiveCategories
from django.forms import inlineformset_factory
from samples_manager.fields import ListTextWidget
from django.utils.safestring import mark_safe
import logging 

OPTIONS = (
            ("5x5 mm²", "5x5 mm²"),
            ("10x10 mm²", "10x10 mm²"),
            ("20x20 mm²", "20x20 mm²"),
            )

ACTIVE_OPTIONS = (
            ("Cold box", "Cold box irradiation (-25°C)"),
            ("Cryostat", "Cryostat (< 5 K)"),
            ("Room temperature", "Room temperature (~ 20 °C)"),
            )



class ExperimentsForm1(forms.ModelForm):
    cern_experiment = forms.CharField(required=True)
    def __init__(self, *args, **kwargs):
        _cern_experiment_list = kwargs.pop('data_list', None)
        super(ExperimentsForm1, self).__init__(*args, **kwargs)
        self.fields['responsible'].empty_label = None
        self.fields['title'].label='Irradiation experiment title *'
        self.fields['description'].label='Description *'
        self.fields['cern_experiment'].widget = ListTextWidget(data_list=_cern_experiment_list, name='cern_experiment_-list')
        self.fields['cern_experiment'].label='CERN experiment/Projects *'
        self.fields['responsible'].label='Responsible person *'
        self.fields['constraints'].required = False
        self.fields['availability'].label= 'Availability *'
        self.fields['availability'] = forms.DateField(('%d/%m/%Y',),widget=forms.DateInput(format='%d/%m/%Y',attrs={'placeholder': 'When your samples will be available for irradiation'} ) )
    class Meta:
        model = Experiments
        exclude = ('category','number_samples','comments','regulations_flag')
        fields = ['title','description','cern_experiment','responsible','availability','constraints']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Please, provide a unique title for your irradiation experiment'}),
            'description': forms.Textarea(attrs={'placeholder': 'Please, provide a short description of your experiment', 'rows':2}),
            'constraints': forms.TextInput(attrs={'placeholder': 'Provide any time constraints, e.g. test beam'}),
        }

def validate_negative(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is negative'),
            params={'value': value},
        )
class ExperimentsForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperimentsForm2, self).__init__(*args, **kwargs)
        self.fields['number_samples'] = forms.IntegerField(min_value=0)
        self.fields['number_samples'].label='Number of samples *'
        self.fields['category'].label='Category *'
    class Meta:
        model = Experiments
        exclude = ('title','description','cern_experiment','responsible','availability','constraints','comments','regulations_flag')
        fields = ['number_samples','category']

class ExperimentsForm3(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperimentsForm3, self).__init__(*args, **kwargs)
        self.fields['comments'].required = False
        self.fields['regulations_flag'].required = True
        self.fields['regulations_flag'].label=mark_safe('<a target="_blank" style="color:black; text-decoration: underline;" href="/samples_manager/regulations/">Please, accept terms and conditions * </a>')
    class Meta:
        model = Experiments
        exclude = ('title','description','responsible','cern_experiment''availability','constraints','category','number_samples')
        fields = ['comments','regulations_flag']
        widgets = {
           'comments': forms.Textarea(attrs={'placeholder': 'Any additional comments?', 'rows':4}),
        }


def get_fluences(experiment_id):
    fluences = ReqFluences.objects.all().filter( experiment = experiment_id)       
    return fluences
    
def get_materials(experiment_id):
    materials = Materials.objects.all().filter( experiment = experiment_id)       
    return materials

class UsersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Users
        fields = ['name', 'surname', 'email','telephone', 'role']
        widgets = { 
        }

class ReqFluencesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReqFluencesForm, self).__init__(*args, **kwargs)
        self.fields['req_fluence'].label=mark_safe('Requested fluence *<br>(protons/cm²)')

    class Meta:
        model = ReqFluences
        fields = ['id','req_fluence']
        widgets = {
            'req_fluence':  forms.TextInput(attrs={'placeholder': 'e.g. 2E14 '})
        }
        exclude = ('experiment',)

class MaterialsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MaterialsForm, self).__init__(*args, **kwargs)
        self.fields['material'].label='Types of sample *'

    class Meta:
        model = Materials
        fields = ['id','material',]
        widgets = {
            'material':  forms.TextInput(attrs={'placeholder': 'e.g.Silicon'})
        }
        exclude = ('experiment',)
    
class PassiveStandardCategoriesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PassiveStandardCategoriesForm, self).__init__(*args, **kwargs)
        self.fields['irradiation_area_5x5'].label="5x5 mm²"
        self.fields['irradiation_area_10x10'].label="10x10 mm²"
        self.fields['irradiation_area_20x20'].label="20x20 mm²"

    class Meta:
        model = PassiveStandardCategories
        fields = ['id','irradiation_area_5x5','irradiation_area_10x10', 'irradiation_area_20x20']
        exclude = ('experiment',)

class PassiveCustomCategoriesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PassiveCustomCategoriesForm, self).__init__(*args, **kwargs)
        self.fields['passive_category_type'] = forms.ChoiceField(choices = ACTIVE_OPTIONS)
        self.fields['passive_category_type'].label="Type *"
        self.fields['passive_irradiation_area'].label="Irradiation area *"
        self.fields['passive_modus_operandi'].label="Modus operandi *"

    class Meta:
        model = PassiveCustomCategories
        fields = ['id','passive_category_type','passive_irradiation_area','passive_modus_operandi']
        widgets = {
             'passive_modus_operandi': forms.Textarea(attrs={'placeholder': 'please, provide more details','rows':3}),
             'passive_irradiation_area': forms.TextInput(attrs={'placeholder': 'e.g. 25x25 mm²'}),
        }
        exclude = ('experiment',)

class ActiveCategoriesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActiveCategoriesForm, self).__init__(*args, **kwargs)
        self.fields['active_category_type'] = forms.ChoiceField(choices = ACTIVE_OPTIONS)
        self.fields['active_category_type'].label="Type *"
        self.fields['active_irradiation_area'].label="Irradiation area *"
        self.fields['active_modus_operandi'].label=mark_safe('Modus operandi and <a target="_blank" style="color:black; text-decoration: underline;" href="https://ps-irrad.web.cern.ch/ps-irrad/index.php?link=irrad_connectivity.html ">IRRAD connectivity </a> *')

    class Meta:
        model = ActiveCategories
        fields = ['id','active_category_type','active_irradiation_area','active_modus_operandi']
        widgets = {
             'active_modus_operandi': forms.Textarea(attrs={'placeholder': 'Please, provide more details and cabling requirements.','rows':3}),
             'active_irradiation_area': forms.TextInput(attrs={'placeholder': 'e.g. 25x25 mm²'}),
        }
        exclude = ('experiment',)







