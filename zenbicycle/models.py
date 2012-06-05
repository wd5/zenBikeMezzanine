# -*- coding: utf-8 -*-
#from put.zenbicycle.fields import ThumbnailImageField
from django.db import models


class color(models.Model):
    name = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

# класс модель вела 
class AbstractModelBicycle(models.Model):
    modelName = models.CharField(max_length=255)
    firm = models.CharField(max_length=255)
    year = models.IntegerField()
    #img = ThumbnailImageField(upload_to='/img') # картинка
    features = models.TextField(blank=True) # характеринстика
    link = models.TextField(blank=True)
    def __unicode__(self):
        return self.firm + ' ' + self.modelName

# основной класс вела
class bicycle(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    numberFrame = models.CharField(max_length=255)
    #img = ThumbnailImageField(upload_to='/img') # картинка
    comment = models.TextField(blank=True)
    colorBicycle = models.ManyToManyField(color, blank=True, null=True)
    modelBicycle = models.ForeignKey(AbstractModelBicycle)
    def __unicode__(self):
        return self.title

class incident(models.Model):
    date = models.DateTimeField()
    placeText = models.CharField(max_length=255)
    placeOnMap = models.CharField(max_length=255)
    comment = models.TextField()
    def __unicode__(self):
        return self.comment
