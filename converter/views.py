# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from transformation.transformation.OSTN02 import webgui_convert

def index(request):
    return render(request, 'converter/index.html')

def map(request):
    system = request.POST['system']

    if system == 'NE':
        lat,lng = webgui_convert(float(request.POST['1']), float(request.POST['4']))
    elif system == 'DMS':
        lat = float(request.POST['1']) + (float(request.POST['2'])/60) + (float(request.POST['3'])/360)
        lng = float(request.POST['4']) + (float(request.POST['5']) / 60) + (float(request.POST['6']) / 360)
    else:
        lat = float(request.POST['1'])
        lng = float(request.POST['4'])

    template = loader.get_template('converter/map.html')
    context = RequestContext(request, {'lat': lat, 'long': lng, 'system': system})
    return HttpResponse(template.render(context))


