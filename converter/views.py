# Create your views here.
import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
import numpy

from transformation.transformation.OSTN02 import webgui_convert


def handle_uploaded_file(f):

    i=0
    csvin = csv.reader(f)
    row = list(csvin)
    totalrows = len(row)
    points = numpy.zeros((totalrows,4 ))
    csvin = csv.reader(f)
    for row in csvin:

        points[i][0] = row[0]
        points[i][1] = row[1]
        points[i][2] = row[2]
        points[i][3] = row[3]
        i = i+1

    return points, totalrows

#with open('c:\users\matt\projects\webgui\data.txt', 'wb+') as destination:
#  for chunk in f.chunks():
#       destination.write(chunk)


def index(request):
    return render(request, 'converter/index.html')


def map(request):
    system = request.POST['system']
    convert = False
    totalrows = 1
    if "convert" in request.POST.keys():
        convert = True
    if "usefile" in request.POST.keys():
        points, totalrows = handle_uploaded_file(request.FILES['path'])
        print(points)
        lat = numpy.zeros(totalrows)
        lng = numpy.zeros(totalrows)
        height = numpy.zeros(totalrows)
        label = numpy.zeros(totalrows)
        for i in range(0, totalrows, 1):
            lat[i], lng[i], height[i] = webgui_convert(points[i][1], points[i][2], points[i][3], convert)
            label[i] = points[i][0]
        print(lat,lng,height)
        print(zip(lat, lng, label))
    else:
        lat = numpy.zeros(1)
        lng = numpy.zeros(1)
        height = numpy.zeros(1)
        label = 'Point'
        if system == 'NE':
            lat[0], lng[0], height[0] = webgui_convert(float(request.POST['east']), float(request.POST['north']),
                                              float(request.POST['height']), convert)
            print(lat, lng, height)
        elif system == 'DMS':
            lat[0] = float(request.POST['latd']) + (float(request.POST['latm']) / 60) + (
                float(request.POST['lats']) / 3600)
            lng[0] = float(request.POST['lngd']) + (float(request.POST['lngm']) / 60) + (
                float(request.POST['lngs']) / 3600)
            height[0] = float(request.POST['height'])

        else:
            lat[0] = float(request.POST['latdd'])
            lng[0] = float(request.POST['lngdd'])
            height[0] = float(request.POST['height'])


    template = loader.get_template('converter/map.html')
    context = RequestContext(request, {'latlist': lat, 'longlist': lng, 'system': system, 'totalrows': xrange(totalrows), 'lat_and_long_label': zip(lat, lng, label)})
    return HttpResponse(template.render(context))


