# -*- coding: utf-8 -*-
#from put.zenbicycle.fields import ThumbnailImageField
from django.db import models
from mezzanine.core.fields import FileField
from mezzanine.core.models import Orderable, RichText
from mezzanine.pages.models import Page
from django.utils.translation import ugettext, ugettext_lazy as _

class color(models.Model):
    name = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

# класс модель вела 
class AbstractModelBicycle(Page):
    modelName = models.CharField(max_length=255)
    firm = models.ForeignKey("bicycleFirm")
    year = models.IntegerField()
    image = models.CharField(_("Image"), max_length=100, blank=True, null=True)
    #img = models.ImageField(upload_to="abstractBicycle")
    #img = ThumbnailImageField(upload_to='/img') # картинка
    features = models.TextField(blank=True) # характеринстика
    link = models.TextField(blank=True)
    def __unicode__(self):
        return self.firm + ' ' + self.modelName

# основной класс вела
class bicycle(Page):
   # title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    numberFrame = models.CharField(max_length=255)
    #img = ThumbnailImageField(upload_to='/img') # картинка
    comment = models.TextField(blank=True)
    colorBicycle = models.ManyToManyField(color, blank=True, null=True)
    modelBicycle = models.ForeignKey(AbstractModelBicycle)
    def __unicode__(self):
        return self.title

class bicycleList(Page, RichText):
    name = models.CharField(max_length=255)
    bicl = models.ForeignKey(bicycle)
    def __unicode__(self):
        return self.name

class incident(models.Model):
    date = models.DateTimeField()
    placeText = models.CharField(max_length=255)
    placeOnMap = models.CharField(max_length=255)
    comment = models.TextField()
    def __unicode__(self):
        return self.comment

class bicycleFirm(models.Model):
    firmName = models.CharField(max_length=255)
    countryOfOrigin = models.CharField(max_length=255, blank=True, null=True)
    def __unicode__(self):
        return self.firmName