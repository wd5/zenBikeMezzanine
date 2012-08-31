# -*- coding: utf-8 -*-
#from put.zenbicycle.fields import ThumbnailImageField
from django.db import models
from django.db.models import CharField
from mezzanine.core.fields import FileField
from mezzanine.core.models import Orderable, RichText
from mezzanine.pages.models import Page
from mezzanine.utils.models import AdminThumbMixin
from mezzanine.galleries.models import GalleryImage
from django.utils.translation import ugettext, ugettext_lazy as _
from sorl.thumbnail import ImageField
from sorl.thumbnail.shortcuts import get_thumbnail

class color(models.Model):
    name = models.CharField(max_length=55, unique=True)
    def __unicode__(self):
        return self.name

class imagesList(models.Model):
    comment = models.CharField(max_length=255)
    image = ImageField(upload_to="bike")
    bike = models.ForeignKey("AbstractModelBicycle")

# класс модель вела 
class AbstractModelBicycle(models.Model):
    modelName = models.CharField(max_length=255)
    firm = models.ForeignKey('bicycleFirm')
    year = models.IntegerField(blank=True, null=True)
    image = models.CharField(_("Image"), max_length=100, blank=True, null=True)

    # image = CharField(_("Image"), max_length=100, blank=True, null=True)
    #img = models.ImageField(upload_to="abstractBicycle")
    #img = ThumbnailImageField(upload_to='/img') # картинка
    features = models.TextField(blank=True) # характеринстика
    sitelink = models.TextField(blank=True)
    def get_thumbnail_html(self):
        img = self.image
        img_resize_url = unicode(get_thumbnail(img, '100x100').url)
        html = '<a class="image-picker" href="%s"><img src="%s" alt="%s"/></a>'
        return html % (self.image.url, img_resize_url, self.modelName)
    get_thumbnail_html.short_description = u'Миниатюра'
    get_thumbnail_html.allow_tags = True

    def __unicode__(self):
        return self.modelName

# основной класс вела
class bicycle(models.Model):
    owner = models.CharField(max_length=255)
    numberFrame = models.CharField(max_length=255, blank=True, null=True)
    numberID = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    #img = ThumbnailImageField(upload_to='/img') # картинка
    comment = models.TextField(blank=True)
    colorBicycle = models.ForeignKey(color, blank=True)
    modelBicycle = models.ForeignKey(AbstractModelBicycle)
        
    def __unicode__(self):
        return self.modelBicycle.modelName


class incident(models.Model):
    date = models.DateTimeField()
    placeText = models.CharField(max_length=255)
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