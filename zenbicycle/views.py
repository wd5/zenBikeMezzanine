# Create your views here.
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from zenbicycle.models import bicycle, bicycleFirm, color, AbstractModelBicycle
from mezzanine.utils.views import render, set_cookie, paginate
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views import static
from django.shortcuts import redirect, get_object_or_404, render_to_response
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter, A4
from django.core import mail

def bikelist(request, template="pages/bikeListMain.html"):
        context = {
               "bicycles":  bicycle.objects.all(),
           }
        return render(request, template, context)

# bike card
def bike(request, template="pages/bike.html"):
        if 'id' in request.GET and request.GET['id']:
            bid = request.GET['id']
        else:
            raise Http404
        b = get_object_or_404(bicycle, id=bid)
        context = {
            "bicycle": b,
            "bid": bid,
        }
        return render(request, template, context)


def actaddbike(request, template="pages/actaddbike.html"):
        if request.method == 'POST':
            firmId = request.POST['firm']
            f = bicycleFirm.objects.get(id=firmId)
        else:
            firmId = ''

        context = {
            "testinfo": f.firmName,
        }
        return render(request, template, context)

def addbike(request, template="pages/addbike.html"):
    frame_sizes = range(13,25)
    context = {
        "bicycle": "",
        "bicycleFirms": bicycleFirm.objects.all(),
        "colors": color.objects.all(),
        "sizes": frame_sizes,
    }
    return render(request, template, context)

def feeds_bikemodel(request):
    from django.core import serializers
    json_subcat = serializers.serialize("json", AbstractModelBicycle.objects.filter(firm=request.GET['firm']))
    return HttpResponse(json_subcat, mimetype="application/javascript")