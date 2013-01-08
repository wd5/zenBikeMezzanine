
from zenbicycle.models import bicycle, AbstractModelBicycle, bicycleFirm, imagesList, color, bikeListMain, city
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from sorl.thumbnail.admin import AdminImageMixin
from django.utils.translation import ugettext_lazy as _

#class TrackInline(admin.TabularInline):
 #   model = Track
 #   extra = 1
#class bicycleFirmInline(admin.StackedInline):
#    model = bicycleFirm
    #list_display = ('firmName')

class imagesListInline(AdminImageMixin, admin.TabularInline):
    model = imagesList

class AbstractModelBicycleAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('get_thumbnail_html','firm' ,'modelName', 'year')
    list_filter = ('firm',)
    list_display_links =  ['get_thumbnail_html', 'modelName', ]
    inlines = [imagesListInline, ]
    actions = [admin.actions.delete_selected]
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
'''
class bicycleInline(AutocompleteTabularInline ):
    model = bicycle
    extra=0
    related_search_fields={
                'colorBicycle':                 ( 'name', ),
        }
'''
class bicycleAdmin(admin.ModelAdmin):
    list_display = ('modelBicycle', 'numberFrame', 'colorBicycle', 'size_frame', 'brake_type' , 'mainOwner', 'status', 'city', 'numberID', 'moderate')
    list_filter = ('city', 'moderate')
    actions = [admin.actions.delete_selected, 'make_moderate']
    
    def make_moderate(self, request, queryset):
        queryset.update(moderate=True)
    make_moderate.short_description = _("Mark as inspection")
    

 #   class form(forms.ModelForm):
 #       class Meta:
 #           widgets = {
 #               'address': AddressWithMapWidget({'class': 'vTextField'})
 #           }



#class bicycleAdmin( AutocompleteModelAdmin ):
  #  inlines = [inlineColor,]
   # form = bicycleForm
   # related_search_fields={
   #             'colorBicycle':                 ( 'name', ),
   #     }

admin.site.register(bikeListMain, PageAdmin)
admin.site.register(bicycle, bicycleAdmin)
admin.site.register(color)
admin.site.register(city)
#admin.site.register(imagesList)
admin.site.register(AbstractModelBicycle, AbstractModelBicycleAdmin)
admin.site.register(bicycleFirm)
#admin.site.register(bicycleList, PageAdmin)
