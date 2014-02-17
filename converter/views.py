# Create your views here.
import csv

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
import numpy
from django.core.urlresolvers import reverse

from converter.models import Survey, Points, Groups
from transformation.transformation.OSTN02 import webgui_convert


def handle_uploaded_file(f):
    i = 0
    csvin = csv.reader(f)
    row = list(csvin)
    totalrows = len(row)
    label = []
    points = numpy.zeros((totalrows, 3 ))
    csvin = csv.reader(f)
    for row in csvin:
        points[i][0] = row[1]
        points[i][1] = row[2]
        points[i][2] = row[3]
        label.append(row[0])
        i += 1

    return points, totalrows, label


#with open('c:\users\matt\projects\webgui\data.txt', 'wb+') as destination:
#  for chunk in f.chunks():
#       destination.write(chunk)


def index(request):
    return render(request, 'converter/index.html')


def process(request):
    system = request.POST['system']
    convert = False
    totalrows = 1
    s = Survey(name='Test')
    s.save()
    print(s.pk)
    if "convert" in request.POST.keys():
        convert = True
    if "usefile" in request.POST.keys():
        points, totalrows, label = handle_uploaded_file(request.FILES['path'])
        print(points)
        OSGBe = numpy.zeros(totalrows)
        OSGBn = numpy.zeros(totalrows)
        OSGBh = numpy.zeros(totalrows)
        ETRS89lat = numpy.zeros(totalrows)
        ETRS89lng = numpy.zeros(totalrows)
        ETRS89h = numpy.zeros(totalrows)
        input_type = []
        group = []
        for i in range(0, totalrows, 1):
            if i == 0:
                g = Groups(survey=s, colour='FF0000', type='PL')
                print('initial')
                g.save()
                group.append(g.pk)
            else:
                if (int(label[i - 1][-1:]) == int(label[i][-1:]) - 1) or (
                            int(label[i - 1][-1:]) == int(label[i][-1:]) + 9):
                    group.append(g.pk)
                    print('same, do nothing')
                else:
                    g = Groups(survey=s, colour='FF0000', type='PL')
                    g.save()
                    group.append(g.pk)
                    print('change')
            OSGBe[i], OSGBn[i], OSGBh[i] = points[i][0], points[i][1], points[i][2]
            input_type.append('OSGB')
            ETRS89lat[i], ETRS89lng[i], ETRS89h[i] = webgui_convert(points[i][0], points[i][1], points[i][2], convert)
        data = zip(label, OSGBe, OSGBn, OSGBh, ETRS89lat, ETRS89lng, ETRS89h, group, input_type)
        print(data)
    else:
        lat = numpy.zeros(1)
        lng = numpy.zeros(1)
        height = numpy.zeros(1)
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

    for label, OSGBe, OSGBn, OSGBh, ETRS89lat, ETRS89lng, ETRS89h, group, input_type in data:
        p = Points(survey=s, label=label, OSGBe=OSGBe, OSGBn=OSGBn, OSGBh=OSGBh, ETRS89lat=ETRS89lat,
                   ETRS89lng=ETRS89lng, ETRS89h=ETRS89h, group=Groups.objects.get(pk=group), input_type=input_type)
        p.save()
        print(p.pk)
    return HttpResponseRedirect(reverse('converter:review', args=(s.id,)))


def gmap(request, survey_id):
    try:
        survey = Survey.objects.get(pk=survey_id)
        points = Points.objects.filter(survey=survey)
        groups = Groups.objects.filter(survey=survey)

    except Survey.DoesNotExist:
        raise Http404
    return render(request, 'converter/gmap.html', {'survey': survey, 'points': points, 'groups': groups})


def bmap(request, survey_id):
    try:
        survey = Survey.objects.get(pk=survey_id)
        points = Points.objects.filter(survey=survey)
        groups = Groups.objects.filter(survey=survey)

    except Survey.DoesNotExist:
        raise Http404
    return render(request, 'converter/bmap.html', {'survey': survey, 'points': points, 'groups': groups})


def ostreetmap(request, survey_id):
    try:
        survey = Survey.objects.get(pk=survey_id)
        points = Points.objects.filter(survey=survey)
        groups = Groups.objects.filter(survey=survey)

    except Survey.DoesNotExist:
        raise Http404
    return render(request, 'converter/ostreetmap.html', {'survey': survey, 'points': points, 'groups': groups})


def OSmap(request, survey_id):
    try:
        survey = Survey.objects.get(pk=survey_id)
        points = Points.objects.filter(survey=survey)
        groups = Groups.objects.filter(survey=survey)

    except Survey.DoesNotExist:
        raise Http404
    return render(request, 'converter/OS.html', {'survey': survey, 'points': points, 'groups': groups})


def review(request, survey_id):
    try:
        survey = Survey.objects.get(pk=survey_id)
        points = Points.objects.filter(survey=survey)
        groups = Groups.objects.filter(survey=survey)

    except Survey.DoesNotExist:
        raise Http404
    return render(request, 'converter/review.html', {'survey': survey, 'points': points, 'groups': groups})

def update_group(request):
    try:
        print('Hello')
        group = Groups.objects.get(pk=request.POST['group_id'])
        group.type = request.POST['type']
        group.colour = request.POST['colour']
        group.save()
    except Groups.DoesNotExist:
        raise Http404
    return render(request, 'converter/group_update.html')
