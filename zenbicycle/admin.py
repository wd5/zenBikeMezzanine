from zenbicycle.models import bicycle, AbstractModelBicycle
from django.contrib import admin

#class TrackInline(admin.TabularInline):
 #   model = Track
 #   extra = 1

class AbstractModelBicycleAdmin(admin.ModelAdmin):
    list_display = ('firm', 'modelName', 'year')
'''   fieldsets = [
        (None,               {'fields': ['title', 'author']}),
        ('Additional', {'fields': ['img'], 'classes': ['cfffffffffffffffffffffffffffffffffffffffffffffffffffffollapse']}),
    ]
 #   inlines = [TrackInline]
    search_fields= ['title', 'author']
'''

admin.site.register(bicycle)
admin.site.register(AbstractModelBicycle, AbstractModelBicycleAdmin)

