# Create your views here.
from django.template import RequestContext, loader
from zenbicycle.models import bicycle
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
               "test": _("test"),
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
