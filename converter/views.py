# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext

def index(request):
    return render(request, 'converter/index.html')

def map(request):
    lat = request.POST['lat']
    long = request.POST['long']
    template = loader.get_template('converter/map.html')
    context = RequestContext(request, {'lat': lat, 'long': long})
    return HttpResponse(template.render(context))


