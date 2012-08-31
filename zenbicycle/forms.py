from django.forms import forms
from django.forms.models import ModelForm
from zenbicycle.models import color, bicycle

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



  