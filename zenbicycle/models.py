# -*- coding: utf-8 -*-
#from put.zenbicycle.fields import ThumbnailImageField
from django.db import models
from django.db.models import CharField
from mezzanine.core.fields import FileField
from mezzanine.core.models import Orderable, RichText
from mezzanine.pages.models import Page
from mezzanine.utils.models import AdminThumbMixin
from mezzanine.galleries.models import GalleryImage, Gallery
from mezzanine.core.managers import SearchableManager
from django.utils.translation import ugettext, ugettext_lazy as _
from sorl.thumbnail import ImageField
from sorl.thumbnail.shortcuts import get_thumbnail
from django.contrib.auth.models import User

class color(models.Model):
    name = models.CharField(max_length=55, unique=True)
    class Meta:
        verbose_name = _("color")
        verbose_name_plural = _("colors")

    def __unicode__(self):
        return self.name

class city(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")

    def __unicode__(self):
        return self.name

class imagesList(models.Model):
    comment = models.CharField(max_length=255)
    image = ImageField(upload_to="bike")
    bike = models.ForeignKey("AbstractModelBicycle")

class imagesListForBike(models.Model):
    image = ImageField(upload_to="UserBike")
    bike = models.ForeignKey("bicycle", related_name="images")

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

    class Meta:
        verbose_name = _("bike model")
        verbose_name_plural = _("bikes models")

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
class bicycle(models.Model, AdminThumbMixin):
    BRAKE_TYPE_CH = (('d', 'disk'), ('r', 'v-brake'), ('o', 'other'))

    mainOwner = models.ForeignKey(User, verbose_name=_("Owner"), related_name="bikes")
   # owner = models.CharField(max_length=255, blank=True)
    numberFrame = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Frame number"))
    size_frame = models.IntegerField(blank=True, null=True, verbose_name=_("Size frame"))
    numberID = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Extra ID number"), default="-")
   # address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    brake_type = models.CharField(max_length=1, blank=True, choices=BRAKE_TYPE_CH, verbose_name=_("Brake type"))
    #img = ThumbnailImageField(upload_to='/img') # картинка
    comment = models.TextField(blank=True, verbose_name=_("Comment"))
    colorBicycle = models.ForeignKey(color, blank=True, null=True, verbose_name="Color Bicycle")
    modelBicycle = models.ForeignKey(AbstractModelBicycle, verbose_name="Model Bicycle")
    status = models.CharField(max_length=1, choices=(('o', 'owner'),('s', 'stolen')), verbose_name="Status", default='o')
    moderate = models.BooleanField(default=False, verbose_name=_("moderate"))
    city = models.ForeignKey("city", verbose_name=_("City"))
    date_create = models.DateTimeField(auto_now_add=True,verbose_name=_("date create"))

    admin_thumb_field = "image"

    objects = SearchableManager()
    search_fields = ("modelBicycle", "numberFrame", "comment")
    @property
    def get_first_img_url(self):
        if self.images.count() > 0:
            img = self.images.all()[0]
            return img.image.url
        return ""
    
    @property
    def get_brake_type(self):
        r = _('None')
        for ind, t in self.BRAKE_TYPE_CH:
            if self.brake_type == ind:
                r = t
        return r

    @property
    def get_status(self):
        if self.status == 's':
            r = _('stolen')
        else:
            r = _('owner')
        return r

    class Meta:
        verbose_name = _("bicycle")
        verbose_name_plural = _("bicycles")

    def __unicode__(self):
        if self.modelBicycle:
            return self.modelBicycle.modelName
        else:
            return u'%s %s' % (self.id, self.comment)



class incident(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    placeText = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    bike = models.ForeignKey("bicycle", related_name="incidents")
    statement2police = models.BooleanField(default=False)

    def __unicode__(self):
        return self.comment

class bicycleFirm(models.Model):
    firmName = models.CharField(max_length=255, verbose_name=_("Firm name"))
    countryOfOrigin = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Country"))

    class Meta:
        verbose_name = _("firm")
        verbose_name_plural = _("firms")

    def __unicode__(self):
        return self.firmName

class bikeListMain(Page):
    class Meta:
        verbose_name = _("Bike list")
        verbose_name_plural = _("Bike lists")

    

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