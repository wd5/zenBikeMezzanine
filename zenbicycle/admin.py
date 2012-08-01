from zenbicycle.models import bicycle, AbstractModelBicycle, bicycleFirm, imagesList
from mezzanine.pages.admin import PageAdmin
from django.contrib import admin

from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin

from cartridge.shop.forms import ImageWidget
from django.db.models import ImageField
from sorl.thumbnail.admin import AdminImageMixin


#class TrackInline(admin.TabularInline):
 #   model = Track
 #   extra = 1
#class bicycleFirmInline(admin.StackedInline):
#    model = bicycleFirm
    #list_display = ('firmName')
class imagesListInline(AdminImageMixin, admin.TabularInline):
    model = imagesList

class AbstractModelBicycleAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('get_thumbnail_html', 'modelName', 'year')
    list_display_links =  ['modelName', ]
    inlines = [imagesListInline, ]
'''
      list_display = ['get_thumbnail_html', 'title', 'tags']
    list_display_links = ['title', ]

     fieldsets = [
        (None,               {'fields': ['title', 'author']}),
        ('Additional', {'fields': ['img'], 'classes': ['collapse']}),
    ]
 #   inlines = [TrackInline]
    search_fields= ['title', 'author']
'''
    # Save the images formset stored previously.


    # Run again to allow for no images existing previously, with
    # new images added which can be used as defaults for variations.




admin.site.register(bicycle)
#admin.site.register(imagesList)
admin.site.register(AbstractModelBicycle, AbstractModelBicycleAdmin)
admin.site.register(bicycleFirm)
#admin.site.register(bicycleList, PageAdmin)
