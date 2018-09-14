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
STORAGE=(('Room temperature','Room temperature'),('Cold storage <20','Cold storage <20 °C'))
STATUS=(('Registered','Registered'),('Updated','Updated'),('Approved','Approved'),('Ready','Ready'),('InBeam','In beam'),('OutBeam','Out of beam'),('CoolingDown','Cooling down'),('Completed','Completed'), ('InStorage','In Storage'),('OutOfIRRAD','Out of IRRAD'),('Waste','Waste'))
EXPERIMENT_STATUS=(('Registered','Registered'),('Updated','Updated'),('Validated','Validated'),('On going','On going'),('Paused','Paused'),('Completed','Completed')) 
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

ROLE=(('Owner','Owner'),('Operator','Operator'),('Coordinator','Coordinator'),('User','User'))


class Users(models.Model):
    email = models.EmailField(max_length=200)
    name = models.CharField(max_length=200,  null=True)
    surname = models.CharField(max_length=200, null=True)
    telephone = models.CharField(max_length=200, null=True)
    db_telephone = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)
    home_institute = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=100, choices= ROLE, default='User', null=True)
    last_login = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.last_login = timezone.now()
        return super(Users, self).save(*args, **kwargs)


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
    emergency_phone =  models.CharField(max_length=200)
    # these fields should be autofilled
    status=models.CharField(max_length=50, choices=EXPERIMENT_STATUS)
    responsible=models.ForeignKey(Users, related_name='%(class)s_responsible')
    users = models.ManyToManyField(Users)
    created_at = models.DateTimeField(editable=False)
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
    name = models.CharField(max_length=200, unique = True)
    current_location = models.CharField(max_length=100)
    height = models.DecimalField(max_digits=12,decimal_places=3)
    width = models.DecimalField(max_digits=12,decimal_places=3)
    weight = models.DecimalField(max_digits=12,decimal_places=3, null=True)
    comments = models.TextField()
    req_fluence =  models.ForeignKey(ReqFluences)
    material = models.ForeignKey(Materials)
    category = models.CharField(max_length=200)
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
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at= timezone.now()
        self.updated_at = timezone.now()
        return super(Samples, self).save(*args, **kwargs)


class Occupancies(models.Model):
    radiation_length_occupancy =  models.DecimalField(max_digits=9,decimal_places=3)
    nu_coll_length_occupancy =  models.DecimalField(max_digits=9,decimal_places=3)
    nu_int_length_occupancy =  models.DecimalField(max_digits=9,decimal_places=3)
    sample = models.ForeignKey(Samples,null=True)

    def __str__(self):              # __str__ on Python 2
        return str(self.radiation_length_occupancy) + " "+ str(self.nu_coll_length_occupancy) +  " "+ str(self.nu_int_length_occupancy)

class Dosimeters(models.Model):
    dos_id= models.CharField(max_length=50, null= True, unique = True)
    responsible = models.ForeignKey(Users, related_name="%(class)s_responsible",  null= True)
    current_location = models.CharField(max_length=100, null= True)
    length = models.DecimalField(max_digits=18,decimal_places=6, null= True)
    height = models.DecimalField(max_digits=18,decimal_places=6, null= True)
    width =  models.DecimalField(max_digits=18,decimal_places=6, null= True)
    weight = models.DecimalField(max_digits=21,decimal_places=9, null=True)
    foils_number = models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=50, choices=STATUS)
    dos_type = models.CharField(max_length=50, choices=DOSIMETER_CATEGORY)
    comments = models.TextField(null=True)
    box = models.ForeignKey(Boxes, null=True)
    created_at=models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    created_by = models.ForeignKey(Users,related_name="%(class)s_created_by", null=True)
    updated_by = models.ForeignKey(Users, related_name="%(class)s_updated_by", null=True)
    last_location = models.CharField(max_length=100,null=True)

    def __str__(self):              # __str__ on Python 2
        return self.dos_id

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at= timezone.now()
        self.updated_at = timezone.now()
        return super(Dosimeters, self).save(*args, **kwargs)


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
        return  str(self.atomic_symbol)+ "("+ str(self.atomic_number) +")"

class Compound(models.Model):
    name = models.CharField(max_length=30, unique = True)
    density = models.DecimalField(max_digits=16,decimal_places=7,null = True)

    def __str__(self):              # __str__ on Python 2
        return self.name

class CompoundElements(models.Model):
    element_type = models.ForeignKey(MaterialElements)
    percentage = models.DecimalField(max_digits=15, decimal_places=4)
    compound = models.ForeignKey(Compound, null = True)

class Layers(models.Model):
    name = models.CharField(max_length=20)
    length = models.DecimalField(max_digits=26,decimal_places=6)
    element_type = models.ForeignKey(MaterialElements,null = True)
    compound_type = models.ForeignKey(Compound,null = True)
    density = models.DecimalField(max_digits=9,decimal_places=3,null = True)
    percentage = models.DecimalField(max_digits=8,decimal_places=4, null = True)
    sample = models.ForeignKey(Samples, null = True)

    def __str__(self):             # __str__ on Python 2
        return str(self.name)

class Irradiation(models.Model):
    sample = models.ForeignKey(Samples, null = True)
    dosimeter = models.ForeignKey(Dosimeters, null = True)
    date_in = models.DateTimeField(blank=True, null=True)
    date_out = models.DateTimeField(blank=True, null=True)
    table_position = models.CharField(max_length=50, null=True)
    irrad_table = models.CharField(max_length=50)
    accumulated_fluence =  models.DecimalField(max_digits=30,decimal_places=6, null=True)
    created_at = models.DateTimeField(editable=False,null=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(Users,related_name="%(class)s_created_by", null=True)
    updated_by = models.ForeignKey(Users, related_name="%(class)s_updated_by", null=True)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):             # __str__ on Python 2
        return str(self.sample) + str(self.dosimeter)
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at= timezone.now()
        self.updated_at = timezone.now()
        return super(Irradiation, self).save(*args, **kwargs)

class ArchiveExperimentSample(models.Model):
    timestamp = models.DateTimeField(editable=False)
    experiment = models.ForeignKey(Experiments, null=True)
    sample = models.ForeignKey(Samples, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.timestamp= timezone.now()
        return super(ArchiveExperimentSample, self).save(*args, **kwargs)













