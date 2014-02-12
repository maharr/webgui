from django.db import models

class Survey(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Points(models.Model):
    survey = models.ForeignKey(Survey)
    label = models.CharField(max_length=50)
    OSGBe = models.FloatField()
    OSGBn = models.FloatField()
    OSGBh = models.FloatField()
    ETRS89lat = models.FloatField()
    ETRS89lng = models.FloatField()
    ETRS89h = models.FloatField()
    group = models.PositiveIntegerField()
    input_type = models.CharField(max_length=6)
    def __unicode__(self):
        return self.survey

# Create your models here.
