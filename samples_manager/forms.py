# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets   
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm,DateTimeInput,Textarea
from .models import Experiments,Users, ReqFluences,Materials,PassiveStandardCategories,PassiveCustomCategories,ActiveCategories,Samples,Compound,CompoundElements, Layers,Dosimeters, Irradiation, UserPreferences
from django.forms.models import inlineformset_factory
from samples_manager.fields import ListTextWidget
from django.utils.safestring import mark_safe
import logging 
from django.forms.models import BaseInlineFormSet

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
            )

IRRAD_TABLES = (
                ("", "Select IRRAD table"),
                ("Shuttle", "Shuttle"),
                ("IRRAD3", "IRRAD3"),
                ("IRRAD5", "IRRAD5"),
                ("IRRAD7", "IRRAD7"),
                ("IRRAD9", "IRRAD9"),
                ("IRRAD11", "IRRAD11"),
                ("IRRAD13", "IRRAD13"),
                ("IRRAD15", "IRRAD15"),
                ("IRRAD17", "IRRAD17"),
                ("IRRAD19", "IRRAD19"),
                )
    
TABLE_POSITIONS = (
                    ("", "Select position"),
                    ("Center", "Center"),
                    ("Left", "Left"),
                    ("Right", "Right"),
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
        self.fields['emergency_phone'].label = 'Emergency telephone number*'
        self.fields['emergency_phone'].required = True
        self.fields['constraints'].required = False
        self.fields['availability'] = forms.DateField(('%d/%m/%Y',),widget=forms.DateInput(format='%d/%m/%Y',attrs={'placeholder': 'When your samples will be available for irradiation'} ) )
        self.fields['availability'].label= 'Availability *'

    class Meta:
        model = Experiments
        exclude = ('category','number_samples','comments','regulations_flag','irradiation_type')
        fields = ['title','description','cern_experiment','responsible','emergency_phone','availability','constraints']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Please, provide a unique title for your irradiation experiment'}),
            'description': forms.Textarea(attrs={'placeholder': 'Please, provide a short description of your experiment', 'rows':2}),
            'constraints': forms.TextInput(attrs={'placeholder': 'Please,provide any time constraints, e.g. test beam'}),
            'emergency_phone': forms.TextInput(attrs={'placeholder': 'Please, provide a telephone number in case of emergency'}),
        }
    def checking_unique(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data['title']
        experiments = Experiments.objects.all()
        titles =[]
        for exp in experiments:
            titles.append(exp.title)
        if title in titles:
            print("title exists")
            return False
        return True

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
        self.fields['regulations_flag'].label=mark_safe('<a target="_blank" style="color:black; text-decoration: underline;" href="/samples_manager/regulations/">Please, accept terms and conditions *</a> <a target="_blank" href="/samples_manager/regulations/"><i class="info circle icon"></i></a>')
    class Meta:
        model = Experiments
        exclude = ('title','description','responsible','cern_experiment''availability','constraints','category','number_samples','irradiation_type')
        fields = ['comments','regulations_flag']
        widgets = {
           'comments': forms.Textarea(attrs={'placeholder': 'Any additional comments?', 'rows':4}),
        }

class ExperimentStatus(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperimentStatus, self).__init__(*args, **kwargs)
        self.fields['status'].label = "Choose status:"
    class Meta:
        model = Experiments
        fields = ['status']

class IrradiationStatus(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IrradiationStatus, self).__init__(*args, **kwargs)
        self.fields['status'].label = "Choose status:"
    class Meta:
        model = Irradiation
        fields = ['status']

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
        self.fields['telephone'].required = False

    class Meta:
        model = Users
        fields = ['name', 'surname', 'email','telephone', 'role']
        exclude = ('db_telephone', 'department', 'home_institute', 'last_login', )

class ReqFluencesFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(ReqFluencesFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        if self.has_changed() == False:
            raise forms.ValidationError('Please add at least one item to fluences.')

class ReqFluencesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReqFluencesForm, self).__init__(*args, **kwargs)
        self.fields['req_fluence'].label=mark_safe('Requested fluence * (protons/cm²)')

    class Meta:
        model = ReqFluences
        fields = ['id','req_fluence']
        widgets = {
            'req_fluence':  forms.NumberInput(),
        }
        exclude = ('experiment',)

class MaterialsFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(MaterialsFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        if self.has_changed() == False:
            raise forms.ValidationError('Please add at least one item to samples type.')

class MaterialsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MaterialsForm, self).__init__(*args, **kwargs)
        self.fields['material'].label=mark_safe('Types of samples *')

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
        self.fields['set_id'] = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'e.g.SET-001029'}))
        self.fields['set_id'].label= mark_safe('SET ID <span style="color: #F00; text-align:justify">Only if your sample has already an assigned SET ID (e.g. from previous irradiation)</span>')
        self.fields['set_id'].required = False
        self.fields['name'].label= 'Sample Name *'
        self.fields['weight'].label= 'Weight (kg) '
        self.fields['weight'].required = False
        self.fields['material'] = forms.ModelChoiceField(queryset=get_materials(self.experiment_id))
        self.fields['material'].label= 'Type of sample *'

    class Meta:
            model = Samples
            exclude = ('comments','req_fluence','category','current_location', 'storage', 'height','width')
            fields = ['material','name','set_id', 'weight']
            widgets = {
                'description': forms.TextInput(attrs={'placeholder': 'Provide a name or description for your sample. E.g. silicon detector 1'}),
                'weight': forms.NumberInput(attrs={'placeholder': 'Please, provide the weight if this is above 1 Kg'}),
            }

    def checking_unique_sample(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data['name']
        print(name)
        unique = True
        samples =  Samples.objects.all()
        names =[]
        for sample in samples:
            names.append(sample.name)
        if name in names:
            print("name exists")
            unique = False
        return unique

class SamplesForm2(ModelForm):
    def __init__(self, *args, **kwargs):
        self.experiment_id = kwargs.pop('experiment_id')
        super(SamplesForm2, self).__init__(*args, **kwargs)
        self.fields['height'].label= 'Total height (mm) *'
        self.fields['width'].label= 'Total width (mm) *'

    class Meta:
            model = Samples
            exclude = ('comments','req_fluence','category','current_location','storage','material','name','set_id','weight')
            fields = ['height','width']

class SamplesForm3(ModelForm):
    def __init__(self, *args, **kwargs):
            self.experiment_id = kwargs.pop('experiment_id')
            super(SamplesForm3, self).__init__(*args, **kwargs)
            self.fields['req_fluence'] = forms.ModelChoiceField(queryset=get_fluences(self.experiment_id))
            self.fields['req_fluence'].label= 'Requested fluence *'
            self.fields['category'].label= 'Category *'
            self.fields['category'] = forms.ChoiceField(choices=get_categories(self.experiment_id))
            self.fields['current_location'].label= 'Current location *'
            self.fields['comments'].required = False

    class Meta:
            model = Samples
            exclude = ('name','set_id','height','width', 'weight','material')
            fields = ['req_fluence','category','storage','current_location','comments']
            widgets = {
                'current_location':  forms.TextInput(attrs={'placeholder': 'e.g. Bld. 28 or Out of CERN'}),
                'comments': forms.Textarea(attrs={'placeholder': 'Any additional comments  e.g some emergency phone', 'rows':2}),
            }

class LayersFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(LayersFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        if self.has_changed() == False:
            raise forms.ValidationError('Please add at least one layer.')

class LayersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LayersForm, self).__init__(*args, **kwargs)
        self.fields['name'].label= 'Name *'
        self.fields['length'].label= 'Length (mm) *'
        self.fields['compound_type'].label= 'Element or Compound'
        self.fields['compound_type'].widget.attrs = {'class': 'select_element'}
        
    class Meta:
        model = Layers
        fields = ['id','name', 'length','compound_type']
        exclude = ('sample','percentage','element_type','density')
        widgets = {
                'name':  forms.TextInput(attrs={'placeholder': 'e.g. L1'}),
                'comments': forms.Textarea(attrs={'placeholder': 'Any additional comments?', 'rows':2}),
            }


class DosimetersForm1(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DosimetersForm1, self).__init__(*args, **kwargs)
        self.fields['dos_id'] = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'e.g.DOS-002929'}))
        self.fields['dos_id'].label = "Dosimeter ID"
        self.fields['dos_id'].required  = False
        self.fields['length'].required = False
        self.fields['length'].label = "Length (mm)"
        self.fields['height'].required = False
        self.fields['height'].label = "Height (mm)"
        self.fields['width'].required = False
        self.fields['width'].label = "Width (mm)"
        self.fields['weight'].required = False
        self.fields['weight'].label = "Weight (g)"
        self.fields['dos_type'].label = "Dosimeter type"
        self.fields['foils_number'].required = False

    class Meta:
        model = Dosimeters
        fields = ['dos_id','length','height','width', 'weight','foils_number','dos_type']
        exclude = ('responsible','current_location','comments')
        widgets = {
                'weight': forms.TextInput(attrs={'placeholder': 'Please, provide weight expecially if it is more than 1 kg'}),
        }

class DosimetersForm2(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DosimetersForm2, self).__init__(*args, **kwargs)
        self.fields['comments'].required = False
        self.fields['responsible'].empty_label = None

    class Meta:
        model = Dosimeters
        fields = ['responsible','current_location','comments']
        exclude = ('dos_id','length','height','width', 'weight','foils_number','dos_type')
        widgets = {
            'current_location': forms.TextInput(attrs={'placeholder': 'e.g. Blg.14 or Out of CERN'}),
            'comments': forms.Textarea(attrs={'rows':3}),
        }


class GroupIrradiationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupIrradiationForm, self).__init__(*args, **kwargs)
        self.fields['dosimeter'].required = True
        self.fields['dosimeter'].empty_label = 'Select dosimeter'
        self.fields['irrad_table'] = forms.ChoiceField(choices = IRRAD_TABLES)
        self.fields['irrad_table'].required = True
        self.fields['table_position'] = forms.ChoiceField(choices = TABLE_POSITIONS)
        self.fields['table_position'].required = False

    class Meta:
        model = Irradiation
        fields = ['dosimeter','irrad_table', 'table_position']
        exclude = ('sample','date_in', 'date_out', 'accumulated_fluence')

class IrradiationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IrradiationForm, self).__init__(*args, **kwargs)
        self.fields['sample'].required = False
        self.fields['dosimeter'].required = False
        self.fields['dosimeter'].empty_label = 'Select dosimeter'
        self.fields['irrad_table'] = forms.ChoiceField(choices = IRRAD_TABLES)
        self.fields['irrad_table'].required = False
        self.fields['table_position'] = forms.ChoiceField(choices = TABLE_POSITIONS)
        self.fields['table_position'].required = False
        self.fields['comments'].required = False
        self.fields['sec'].required = False
        self.fields['fluence_error'].required = False
        self.fields['date_in'] = forms.DateTimeField(('%Y/%m/%d %H:%M',),widget=forms.DateTimeInput(format='%Y/%m/%d %H:%M',attrs={'placeholder': 'Date when samples were in beam'} ) )
        self.fields['date_out'] = forms.DateTimeField(('%Y/%m/%d %H:%M',),widget=forms.DateTimeInput(format='%Y/%m/%d %H:%M',attrs={'placeholder': 'Date when samples came out of beam'} ) )
        self.fields['date_in'].required = False
        self.fields['date_out'].required = False
        self.fields['accumulated_fluence'].required = False
        
    class Meta:
        model = Irradiation
        fields = ['sample','dosimeter','irrad_table', 'table_position', 'sec', 'accumulated_fluence', 'fluence_error','date_in', 'date_out', 'accumulated_fluence', 'comments']
        exclude = ()


class CompoundElementsFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CompoundElementsFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        if self.has_changed() == False:
            raise forms.ValidationError('Please add at least one item.')


class CompoundElementsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompoundElementsForm, self).__init__(*args, **kwargs)
        self.fields['percentage'].label= 'Density (g/cm³)*'

    class Meta:
        model = CompoundElements
        fields = ['id','element_type','percentage',]
        widgets = {}
        exclude = ('compound',)


class CompoundFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CompoundFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        if self.has_changed() == False:
            raise forms.ValidationError('Please add at least one item.')


class CompoundForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompoundForm, self).__init__(*args, **kwargs)
        self.fields['density'].label= 'Density (g/cm³)*'

    class Meta:
        model = Compound
        fields = ['id','name','density']
        widgets = {}
        exclude = ('compound',)

THEME_CHOICES = (
    ('round', 'Round'),
    ('github', 'GitHub'),
    ('default', 'Default'),
    ('amazon', 'Amazon'),
    ('material', 'Material'),
    ('colored', 'Colored'),
    ('bookish', 'Bookish'),
    ('flat', 'Flat'),
)

class PreferencesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PreferencesForm, self).__init__(*args, **kwargs)
        self.fields['global_theme'] = forms.ChoiceField(choices=THEME_CHOICES, widget = forms.Select(attrs={'name': 'global', 'class': 'ui theme dropdown'}))
        self.fields['button_theme'] = forms.ChoiceField(choices=THEME_CHOICES, widget = forms.Select(attrs={'name': 'global', 'class': 'ui theme dropdown secondary'}))

    class Meta:
        model = UserPreferences
        fields = ['global_theme','button_theme',]
        widgets = {}
        exclude = ('user',)
    





