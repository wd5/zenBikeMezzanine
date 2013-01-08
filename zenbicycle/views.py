
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.template import RequestContext, loader, context
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from zenbicycle.forms import addBikeForm, extraAddBikeForm
from zenbicycle.models import bicycle, bicycleFirm, color, AbstractModelBicycle, city, imagesListForBike
from mezzanine.utils.views import render, set_cookie, paginate
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views import static
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.contrib.auth.models import User

from django.core import mail

def bikelist(request, template="pages/bikeListMain.html"):
        context = {
            "bicycles":  bicycle.objects.all(),
        }
        return render(request, template, context)

# bike card
def bike(request, idb, template="pages/bike.html"):
        b = get_object_or_404(bicycle, id=idb)
        s = ""
        img_mode = False
        if b.imageslistforbike_set.count() > 0:
            img_mode = True
            imgs = b.imageslistforbike_set.all()[0]
            s = imgs.image.url

        context = {
            "bicycle": b,
            "img_mode": img_mode,
            "imgs": s,
        }
        return render(request, template, context)

@login_required
def addbike(request, template="pages/addbike.html"):
    if request.method == 'POST':
        form = addBikeForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            b  = form.save(commit=False)
            u = User.objects.get(username=request.user.username)
            b.mainOwner = u
            b.city = city.objects.get(name=cd['city_new'])

            try:
                m = AbstractModelBicycle.objects.get(id=cd['model'])
                b.modelBicycle = m
            except:
                bicycle_firm, crt = bicycleFirm.objects.get_or_create(firmName="NoName")
                bicycle_model, crt = AbstractModelBicycle.objects.get_or_create(modelName="NoName", firm_id=bicycle_firm.id )
                b.modelBicycle = bicycle_model
            b.save()
            if 'img_file' in request.FILES:
                img = imagesListForBike()
                img.bike = b
                img.image = request.FILES['img_file']
                img.save()
            # b.mainOwner =
            return render(request, template, {'commit': True})
    else:
        form = addBikeForm()
    context = {
        "bicycleFirms": bicycleFirm.objects.all(),
        "formset": form,
        "commit": False,
              #  "auth": request.user.is_authenticated(),
        }
    return render(request, template, context)

def feeds_bikemodel(request):
    from django.core import serializers
    json_subcat = serializers.serialize("json", AbstractModelBicycle.objects.filter(firm=request.GET['firm']))
    return HttpResponse(json_subcat, mimetype="application/javascript")