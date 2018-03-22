# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets   
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm,DateTimeInput,Textarea
from .models import Experiments,Users, ReqFluences,Materials,PassiveStandardCategories,PassiveCustomCategories,ActiveCategories,Samples,SamplesElements
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

PARTICLES = (
            ("Protons", "Protons"),
            ("Heavy ions", "Heavy ions"),
            ("Pions", "Pions"),
            ("Neutrons", "Neutrons"),
            ("Electrons", "Electrons"),
            ("Other", "Other"),
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
        exclude = ('category','number_samples','comments','regulations_flag','irradiation_type')
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
        self.fields['irradiation_type'].label='Irradiation type *'
        self.fields['irradiation_type'] = forms.ChoiceField(choices = PARTICLES)
        self.fields['number_samples'] = forms.IntegerField(min_value=0)
        self.fields['number_samples'].label='Number of samples *'
        self.fields['category'].label='Category *'
    class Meta:
        model = Experiments
        exclude = ('title','description','cern_experiment','responsible','availability','constraints','comments','regulations_flag')
        fields = ['irradiation_type','number_samples','category']

class ExperimentsForm3(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperimentsForm3, self).__init__(*args, **kwargs)
        self.fields['comments'].required = False
        self.fields['regulations_flag'].required = True
        self.fields['regulations_flag'].label=mark_safe('<a target="_blank" style="color:black; text-decoration: underline;" href="/samples_manager/regulations/">Please, accept terms and conditions * </a>')
    class Meta:
        model = Experiments
        exclude = ('title','description','responsible','cern_experiment''availability','constraints','category','number_samples','irradiation_type')
        fields = ['comments','regulations_flag']
        widgets = {
           'comments': forms.Textarea(attrs={'placeholder': 'Any additional comments?', 'rows':4}),
        }


def get_fluences(experiment_id):
    fluences = ReqFluences.objects.filter( experiment = experiment_id)    
    return fluences
    
def get_materials(experiment_id):
    materials = Materials.objects.filter( experiment = experiment_id)       
    return materials

def get_categories(experiment_id):
    experiment = Experiments.objects.get(pk = experiment_id)
    if experiment.category == 'Passive Standard':
        category = PassiveStandardCategories.objects.filter( experiment = experiment_id)
        categories = ()
        if category[0].irradiation_area_5x5==True:
            categories  =  categories  + (('Passive standard 5x5 mm²','Passive standard 5x5 mm²'),)
        if category[0].irradiation_area_10x10==True:
            categories =  categories + (('Passive standard 10x10 mm²','Passive standard 10x10 mm²'),)
        if category[0].irradiation_area_20x20==True:
            categories  =  categories  + (('Passive standard 20x20 mm²','Passive standard 20x20 mm²'),)
    elif experiment.category == 'Passive Custom':
        passive_custom_categories = PassiveCustomCategories.objects.filter( experiment = experiment_id)
        categories = ()
        for category in passive_custom_categories: 
            categories = categories  + ((category.passive_category_type+', in irradiation area: '+category.passive_irradiation_area,category.passive_category_type+', in irradiation area: '+category.passive_irradiation_area),)
    elif experiment.category == 'Active':
        active_categories = ActiveCategories.objects.filter( experiment = experiment_id)
        categories = ()
        for category in active_categories: 
            categories = categories  + ((category.active_category_type+', in irradiation area: '+category.active_irradiation_area,category.active_category_type+', in irradiation area: '+category.active_irradiation_area),)
    return categories
    
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

class SamplesForm1(ModelForm):
    def __init__(self, *args, **kwargs):
        self.experiment_id = kwargs.pop('experiment_id')
        super(SamplesForm1, self).__init__(*args, **kwargs)
        self.fields['description'].label= 'Name *'
        self.fields['height'].label= 'Height (mm) *'
        self.fields['width'].label= 'Width (mm) *'
        self.fields['weight'].label= 'Weight (kg) '
        self.fields['material'].label= 'Samples type *'
        self.fields['material'] = forms.ModelChoiceField(queryset=get_materials(self.experiment_id))
    class Meta:
            model = Samples
            exclude = ('comments','req_fluence','category','current_location')
            fields = ['material','description', 'height','width', 'weight']
            widgets = {
                'description': forms.TextInput(attrs={'placeholder': 'Provide a name or description for your sample. E.g. silicon detector 1'}),
                'weight': forms.NumberInput(attrs={'placeholder': 'Please provide weigth especially if it is more that 1 kg'})
            }

class SamplesForm2(ModelForm):
    def __init__(self, *args, **kwargs):
            self.experiment_id = kwargs.pop('experiment_id')
            super(SamplesForm2, self).__init__(*args, **kwargs)
            self.fields['req_fluence'] = forms.ModelChoiceField(queryset=get_fluences(self.experiment_id))
            self.fields['req_fluence'].label= 'Requested fluence *'
            self.fields['category'].label= 'Category *'
            self.fields['category'] = forms.ChoiceField(choices=get_categories(self.experiment_id))
            self.fields['current_location'].label= 'Current location *'
            self.fields['comments'].required = False

    class Meta:
            model = Samples
            exclude = ('description', 'height','width', 'weight','material')
            fields = ['req_fluence','category','current_location','comments']
            widgets = {
                'current_location':  forms.TextInput(attrs={'placeholder': 'e.g. Bld. 28 or Out of CERN'}),
                'comments': forms.Textarea(attrs={'placeholder': 'Any additional comments?', 'rows':2}),
            }


class SamplesElementsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SamplesElementsForm, self).__init__(*args, **kwargs)
        self.fields['element_type'].label=mark_safe('Material element')
        self.fields['element_length'].label=mark_safe('Length')

    class Meta:
         model = SamplesElements
         fields = ['id','element_type', 'element_length',]
         exclude = ('sample',)




