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
from django.contrib.auth.models import User

class color(models.Model):
    name = models.CharField(max_length=55, unique=True)
    
    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return self.name

class city(models.Model):
    name = models.CharField(max_length=100)
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
    #image = models.CharField(_("Image"), max_length=100, blank=True, null=True)

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
        if self.year <> None:
            return u'%s %s %s' % (self.firm.firmName, self.modelName, self.year)
        else:
            return u'%s %s' % (self.firm.firmName, self.modelName)
        

# основной класс вела
class bicycle(models.Model):
    mainOwner = models.ForeignKey(User)
   # owner = models.CharField(max_length=255, blank=True)
    numberFrame = models.CharField(max_length=255, blank=True, null=True)
    size_frame = models.IntegerField(blank=True, null=True)
    numberID = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    brake_type = models.CharField(max_length=1, blank=True, choices=(('d', 'disk'), ('r', 'v-brake'), ('o', 'other')))
    #img = ThumbnailImageField(upload_to='/img') # картинка
    comment = models.TextField(blank=True)
    colorBicycle = models.ForeignKey(color, blank=True, null=True)
    modelBicycle = models.ForeignKey(AbstractModelBicycle)
    status = models.CharField(max_length=1, choices=(('o', 'owner'),('s', 'stolen')))
    incidents = models.ManyToManyField('incident', blank=True, null=True)
    moderate = models.BooleanField(default=False)
    city = models.ForeignKey("city")

    def __unicode__(self):
        if self.modelBicycle:
            return self.modelBicycle.modelName
        else:
            return u'%s %s' (self.id, self.comment)



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

class bikeListMain(Page):
    bicycles = bicycle.objects.all()
    test = "test 444"
    class Meta:
        verbose_name = "Bike list"
        verbose_name_plural = "Bike lists"


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