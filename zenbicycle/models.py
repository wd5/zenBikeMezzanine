# -*- coding: utf-8 -*-
#from put.zenbicycle.fields import ThumbnailImageField
from django.db import models
from django.db.models import CharField
from mezzanine.core.fields import FileField
from mezzanine.core.models import Orderable, RichText
from mezzanine.pages.models import Page
from mezzanine.utils.models import AdminThumbMixin
from django.utils.translation import ugettext, ugettext_lazy as _
from sorl.thumbnail import ImageField

class color(models.Model):
    name = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name

class imagesList(models.Model):
    comment = models.CharField(max_length=255)
    image = ImageField(upload_to="bike")

# класс модель вела 
class AbstractModelBicycle(models.Model):
    modelName = models.CharField(max_length=255)
    firm = models.ForeignKey('bicycleFirm')
    year = models.IntegerField(blank=True, null=True)
    image = models.ForeignKey(imagesList)

    # image = CharField(_("Image"), max_length=100, blank=True, null=True)
    #img = models.ImageField(upload_to="abstractBicycle")
    #img = ThumbnailImageField(upload_to='/img') # картинка
    features = models.TextField(blank=True) # характеринстика
    sitelink = models.TextField(blank=True)
    def __unicode__(self):
        return self.modelName

# основной класс вела
class bicycle(models.Model):
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

'''class Images(Orderable):
    """
    An image for a product - a relationship is also defined with the
    product's variations so that each variation can potentially have
    it own image, while the relationship between the ``Product`` and
    ``ProductImage`` models ensures there is a single set of images
    for the product.
    """

    file = models.ImageField(_("Image"), upload_to="BikeImg")
    description = CharField(_("Description"), blank=True, max_length=100)
    bike = models.ForeignKey("AbstractModelBicycle", related_name="images")

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        order_with_respect_to = "bike"

    def __unicode__(self):
        value = self.description
        if not value:
            value = self.file.name
        if not value:
            value = ""
        return value
'''