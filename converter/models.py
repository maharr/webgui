from django.db import models
from django.db.models import Max

class Survey(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Groups(models.Model):
    survey = models.ForeignKey(Survey)
    colour = models.CharField(max_length=6)
    type = models.CharField(max_length=2)
    def __unicode__(self):
        return self.survey

class Points(models.Model):
    survey = models.ForeignKey(Survey)
    label = models.CharField(max_length=50)
    OSGBe = models.FloatField()
    OSGBn = models.FloatField()
    OSGBh = models.FloatField()
    ETRS89lat = models.FloatField()
    ETRS89lng = models.FloatField()
    ETRS89h = models.FloatField()
    group = models.ForeignKey(Groups)
    input_type = models.CharField(max_length=6)
    def __unicode__(self):
        return self.survey




# Create your models here.
