import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm,DateTimeInput,Textarea
from django.contrib.admin import widgets
from django.utils.translation import ugettext_lazy as _
# Create your models here.

IRRADIATION_TYPES=(('PASSIVE','Passive'),('ACTIVE','Active'))
CATEGORIES=(('5x5','5x5'),('10x10','10x10'),('20x20','20x20'),('Cold irradiation','Cold irradiation'),('Cryogenics','Cryogenics'),('Scanning','Scanning'),('Big setup','Big setup'),('Other','Other'))


class Experiments(models.Model):
    title=models.CharField(max_length=200)
    max_requested_fluence=models.CharField(max_length=100)
    start_date=models.DateTimeField(blank=True, null=True)
    end_date=models.DateTimeField(blank=True, null=True)
    justification=models.TextField('Justification (if any)')
    resources=models.TextField()
    storage=models.CharField(max_length=100)
    irradiation_type=models.CharField(max_length=100,choices=IRRADIATION_TYPES)
    category=models.CharField(max_length=100,choices=CATEGORIES)
    regulations_flag=models.BooleanField()
    planning=models.TextField()
    

    def __unicode__(self):              # __unicode__ on Python 2
        return self.title
    def long_irradiation(self):
        return self.end_date - self.start_date >=datetime.timedelta(days=1)


class Users(models.Model):
    email= models.CharField(max_length=200)
    name= models.CharField(max_length=200)
    surname= models.CharField(max_length=200)
    telephone=models.CharField(max_length=200)
    role=models.CharField(max_length=100)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.name+self.surname

class ExperUsers(models.Model):
     user_id=models.ForeignKey(Users)
     irradiation_id=models.ForeignKey(Experiments)

class Samples(models.Model):
    set_id=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    size=models.CharField(max_length=50)
    weight=models.CharField(max_length=50)
    material=models.CharField(max_length=50)
    requested_fluence=models.CharField(max_length=50)
    cern_experiment=models.CharField(max_length=200)
    location=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    comments=models.TextField()
    experiment_id=models.ForeignKey(Experiments)

class Dosimeters(models.Model):
    dosimeter_id=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    size=models.CharField(max_length=50)
    weight=models.CharField(max_length=50)
    material=models.CharField(max_length=50)
    foils_number=models.CharField(max_length=50)
    density=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    category=models.CharField(max_length=50)
    comments=models.TextField()

class Factors(models.Model):
    samples_size=models.CharField(max_length=50)
    material=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    value=models.CharField(max_length=50)

class Irradiations(models.Model):
    samples_id=models.ForeignKey(Samples)
    dosimeters_id=models.ForeignKey(Dosimeters)
    date_in=models.DateTimeField(blank=True, null=True)
    date_out=models.DateTimeField(blank=True, null=True)
    position=models.CharField(max_length=50)
    sec_in=models.BigIntegerField()
    sec_out=models.BigIntegerField()





    




    











