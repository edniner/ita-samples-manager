# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm,DateTimeInput,Textarea
from django.contrib.admin import widgets
from django.core.validators import MinValueValidator
# Create your models here.

CERN_EXPERIMENTS=(('ATLAS','ATLAS'),('CMS','CMS'), ('ALICE', 'ALICE'),('LHCb', 'LHCb'), ('TOTEM', 'TOTEM'), ('Other','Other'))
CATEGORIES=(('','Please,choose category'),('Passive Standard','Passive Standard'),('Passive Custom','Passive Custom'),('Active','Active'))
STORAGE=(('Room','Room temperature'),('Cold','Cold storage <20 °C'))
STATUS=(('Registered','Registered'),('Updated','Updated'),('Approved','Approved'),('Ready','Ready'),('InBeam','In beam'),('OutBeam','Out of beam'),('CoolingDown','Cooling down'),('Completed','Completed'), ('InStorage','In Storage'),('OutOfIRRAD','Out of IRRAD'),('Waste','Waste'))
EXPERIMENT_STATUS=(('Registered','Registered'),('Updated','Updated'),('Approved','Approved'),('Ready','Ready'),('OnGoing','On going'),('Paused','Paused'),('Completed','Completed')) 
DOSIMETER_CATEGORY=(('Aluminium','Aluminium'),('Film','Film'), ('Diamond','Diamond'), ('Other','Other'))

IRRAD_POSITION=(
                ('IRRAD1_Shuttle',(
                        ('IRRAD1','IRRAD1-Shuttle'),
                    )
                ),
                ('IRRAD3',(
                        ('IRRAD3','No holder'),
                        ('IRRAD3_Left','Left holder'),
                        ('IRRAD3_Center','Center holder'),
                        ('IRRAD3_Right','Right holder'),
                    )
                 ),
                ('IRRAD5',(
                        ('IRRAD5','Cold Box'),
                    )
                 ),
                ('IRRAD7',(
                        ('IRRAD7','No holder'),
                        ('IRRAD7_Left','Left holder'),
                        ('IRRAD7_Center','Center holder'),
                        ('IRRAD7_Right','Right holder'),
                    )
                ),
                ('IRRAD9',(
                        ('IRRAD9','No holder'),
                        ('IRRAD9_Left','Left holder'),
                        ('IRRAD9_Center','Center holder'),
                        ('IRRAD9_Right','Right holder'),
                    )
                 ),
                ('IRRAD11',(
                        ('IRRAD11','Cold Box'),
                    )
                 ),
                ('IRRAD13',(
                        ('IRRAD13','No holder'),
                        ('IRRAD13_Left','Left holder'),
                        ('IRRAD13_Center','Center holder'),
                        ('IRRAD13_Right','Right holder'),
                    )
                 ),
                ('IRRAD15',(
                        ('IRRAD15','Cryostat'),
                    )
                 ),
                ('IRRAD13',(
                        ('IRRAD13','No holder'),
                        ('IRRAD13_Left','Left holder'),
                        ('IRRAD13_Center','Center holder'),
                        ('IRRAD13_Right','Right holder'),
                    )
                 ),
                ('IRRAD17',(
                        ('IRRAD17','No holder'),
                        ('IRRAD17_Left','Left holder'),
                        ('IRRAD17_Center','Center holder'),
                        ('IRRAD17_Right','Right holder'),
                    )
                 ),
                ('IRRAD19',(
                        ('IRRAD19','No holder'),
                        ('IRRAD19_Left','Left holder'),
                        ('IRRAD19_Center','Center holder'),
                        ('IRRAD19_Right','Right holder'),
                    )
                 )
)

ROLE=(('Owner','Owner'),('Operator','Operator'),('Cordinator','Cordinator'),('Basic','Basic User'))


class Users(models.Model):
    email= models.EmailField(max_length=200)
    name= models.CharField(max_length=200,  null=True)
    surname= models.CharField(max_length=200, null=True)
    telephone=models.CharField(max_length=200, null=True)
    role=models.CharField(max_length=100, choices= ROLE, default='Basic User', null=True)

    def __str__(self):              # __str__ on Python 2
        return self.email

def validate_negative(value):
        if value < 0:
            raise ValidationError(
                _('%(value)s is negative'),
                params={'value': value},
            )

class Experiments(models.Model):
    title = models.CharField(max_length=200, unique = True)
    description =  models.TextField()
    cern_experiment = models.CharField(max_length=100)
    availability = models.DateField( null = True)
    constraints =  models.CharField(max_length=2000)
    number_samples = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)])
    comments = models.TextField( null=True ) 
    category=  models.CharField(max_length=100,choices=CATEGORIES, blank=False)
    regulations_flag = models.BooleanField()
    irradiation_type =  models.CharField(max_length=100)
    # these fields should be autofilled
    status=models.CharField(max_length=50, choices=EXPERIMENT_STATUS)
    responsible=models.ForeignKey(Users, related_name='%(class)s_responsible')
    users = models.ManyToManyField(Users)
    created_at=models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    created_by = models.ForeignKey(Users,related_name="%(class)s_created_by", null=True)
    updated_by = models.ForeignKey(Users, related_name="%(class)s_updated_by", null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at= timezone.now()
        self.updated_at = timezone.now()
        return super(Experiments, self).save(*args, **kwargs)
    
    def __str__(self):           # __str__ on Python 2
        return self.title
    def long_irradiation(self):
        return self.end_date - self.start_date >=datetime.timedelta(days=1)
        
class PassiveStandardCategories(models.Model):
    irradiation_area_5x5 = models.BooleanField()
    irradiation_area_10x10 = models.BooleanField()
    irradiation_area_20x20 = models.BooleanField()
    experiment = models.ForeignKey(Experiments, null = True)

    def __str__(self):              # __str__ on Python 2
        return str(self.irradiation_area_5x5)

class PassiveCustomCategories(models.Model):
    passive_category_type = models.CharField(max_length=50)
    passive_irradiation_area =  models.CharField(max_length=50)
    passive_modus_operandi = models.TextField()
    experiment = models.ForeignKey(Experiments, null = True)

    def __str__(self):              # __str__ on Python 2
        return self.passive_category_type


class ActiveCategories(models.Model):
    active_category_type = models.CharField(max_length=50)
    active_irradiation_area =  models.CharField(max_length=50)
    active_modus_operandi = models.TextField()
    experiment = models.ForeignKey(Experiments, null = True)

    def __str__(self):              # __str__ on Python 2
        return self.active_category_type

class ReqFluences(models.Model):
    req_fluence = models.CharField(max_length=50)
    experiment = models.ForeignKey(Experiments, null = True)

    def __str__(self):              # __str__ on Python 2
        return self.req_fluence


class Materials(models.Model):
    material = models.CharField(max_length=50)
    experiment = models.ForeignKey(Experiments, null = True)

    def __str__(self):              # __str__ on Python 2
        return self.material


class Boxes(models.Model):
    box_id=models.CharField(max_length=50)
    description=models.CharField(max_length=200, null=True)
    responsible=models.ForeignKey(Users, related_name='%(class)s_responsible')
    current_location = models.CharField(max_length=100)
    last_location = models.CharField(max_length=100)
    length = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    width = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    created_at=models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    created_by = models.ForeignKey(Users,related_name="%(class)s_created_by", null=True)
    updated_by = models.ForeignKey(Users, related_name="%(class)s_updated_by", null=True)

    def __str__(self):             # __str__ on Python 2
        return self.box_id
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at= timezone.now()
        self.updated_at = timezone.now()
        return super(Boxes, self).save(*args, **kwargs)


class Samples(models.Model):
    set_id = models.CharField(max_length=50, null = True,  unique = True)
    description = models.CharField(max_length=200, unique = True)
    current_location = models.CharField(max_length=100)
    height = models.DecimalField(max_digits=12,decimal_places=6)
    width = models.DecimalField(max_digits=12,decimal_places=6)
    weight = models.DecimalField(max_digits=12,decimal_places=6, null=True)
    comments = models.TextField()
    req_fluence =  models.ForeignKey(ReqFluences)
    material = models.ForeignKey(Materials)
    category = models.CharField(max_length=50)
    storage = models.CharField(max_length=50, choices=STORAGE)
    #samples characteristics
    status = models.CharField(max_length=50, choices=STATUS)
    last_location = models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    experiment = models.ForeignKey(Experiments,null=True)
    box = models.ForeignKey(Boxes,null=True)
    created_by = models.ForeignKey(Users,related_name="%(class)s_created_by", null=True)
    updated_by = models.ForeignKey(Users, related_name="%(class)s_updated_by", null=True)

    def __str__(self):              # __str__ on Python 2
        return self.description

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at= timezone.now()
        self.updated_at = timezone.now()
        return super(Samples, self).save(*args, **kwargs)


class MaterialElements(models.Model):
    atomic_number = models.PositiveIntegerField()
    atomic_symbol = models.CharField(max_length=5)
    atomic_mass = models.DecimalField(max_digits=15,decimal_places=10)
    density = models.DecimalField(max_digits=9,decimal_places=7)
    min_ionization = models.DecimalField(max_digits=4,decimal_places=3)
    nu_coll_length = models.DecimalField(max_digits=4,decimal_places=1)
    nu_int_length = models.DecimalField(max_digits=4,decimal_places=1)
    pi_coll_length = models.DecimalField(max_digits=4,decimal_places=1)
    pi_int_length = models.DecimalField(max_digits=4,decimal_places=1)
    radiation_length = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):              # __str__ on Python 2
        return self.atomic_symbol 

class SamplesLayers(models.Model):
    name = models.CharField(max_length=20)
    length = models.DecimalField(max_digits=20,decimal_places=6)
    sample = models.ForeignKey(Samples, null = True)

class SamplesElements(models.Model):
    element_type = models.ForeignKey(MaterialElements)
    percentage = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)])
    layer = models.ForeignKey(SamplesLayers, null = True)


class Layers(models.Model):
    name = models.CharField(max_length=20)
    length = models.DecimalField(max_digits=20,decimal_places=6)
    element_type = models.ForeignKey(MaterialElements)
    percentage = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)])
    sample = models.ForeignKey(Samples, null = True)
    




    











