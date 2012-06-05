# -*- coding: utf-8 -*-
#from put.zenbicycle.fields import ThumbnailImageField
from django.db import models
from mezzanine.core.fields import FileField
from mezzanine.core.models import Orderable, RichText
from mezzanine.pages.models import Page

class color(models.Model):
    name = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

# класс модель вела 
class AbstractModelBicycle(Page, RichText):
    modelName = models.CharField(max_length=255)
    firm = models.CharField(max_length=255)
    year = models.IntegerField()
    img = models.ImageField(upload_to="abstractBicycle")
    #img = ThumbnailImageField(upload_to='/img') # картинка
    features = models.TextField(blank=True) # характеринстика
    link = models.TextField(blank=True)
    def __unicode__(self):
        return self.firm + ' ' + self.modelName

# основной класс вела
class bicycle(Page, RichText):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    numberFrame = models.CharField(max_length=255)
    #img = ThumbnailImageField(upload_to='/img') # картинка
    comment = models.TextField(blank=True)
    colorBicycle = models.ManyToManyField(color, blank=True, null=True)
    modelBicycle = models.ForeignKey(AbstractModelBicycle)
    def __unicode__(self):
        return self.title

class incident(Page, RichText):
    date = models.DateTimeField()
    placeText = models.CharField(max_length=255)
    placeOnMap = models.CharField(max_length=255)
    comment = models.TextField()
    def __unicode__(self):
        return self.comment
