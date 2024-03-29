from django.forms import forms
from django.forms.fields import CharField, ChoiceField, BooleanField, ImageField, DateField
from django.forms.models import ModelForm, ModelChoiceField
from django.forms.widgets import Textarea, TextInput, HiddenInput, Select, DateInput
import settings
from zenbicycle.models import color, bicycle, city, bicycleFirm
from mezzanine.core.forms import Html5Mixin
from django.utils.translation import ugettext, ugettext_lazy as _

class bicycleForm(ModelForm):
    colorBicycle = forms.Textarea()
    def save(self, force_insert=True, force_update=True, commit=True):
        colorBicycle_name = self.cleaned_data['colorBicycle']
        colorBicycle = color.objects.get_or_create(name=colorBicycle_name)[0]
        self.instance.colorBicycle = colorBicycle
        return super(bicycleForm, self).save(commit=False)

    class Meta:
        model=bicycle
        exclude = ('colorBicycle')


class addBikeForm(Html5Mixin, ModelForm):
    city_new = CharField()
    firm = ModelChoiceField(queryset=bicycleFirm.objects.all(), required=False)
    model = CharField(required=False, widget=Select)
    chk_stolen = BooleanField(required=False)
    img_file = ImageField(required=False)

    # for stolen info
    stolen_address = CharField(required=False)
    stolen_note = CharField(widget=forms.Textarea, required=False)
    stolen_spk_police = BooleanField(required=False)
    stolen_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = bicycle
        fields = ('firm', 'model', 'city_new', 'numberFrame', 'size_frame', 'brake_type', 'colorBicycle', 'comment', 'img_file', 'chk_stolen',  )
        
    def clean_city_new(self):
        cityname = self.data["city_new"]
        try:
            city.objects.get(name=cityname)
        except city.DoesNotExist:
            c = city(name=cityname)
            c.save()
        return cityname


class extraAddBikeForm(addBikeForm):
    pass
    ''' def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fileds['city'].widget = HiddenInput()
    '''







  