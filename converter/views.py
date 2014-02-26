# Create your views here.
import csv

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import numpy
from django.core.urlresolvers import reverse

from converter.models import Survey, Points, Groups
from transformation.transformation.OSTN02 import webgui_convert, webgui_reverse


#text/csv
#application/vnd.ms-excel


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
    s = Survey(name=request.POST['name'])
    s.save()
    print(s.pk)
    if "convert" in request.POST.keys():
        convert = True
    if request.POST['usefile'] == 'True':
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
                g = Groups(survey=s, colour='FF0000', type='PL', single_point=False)
                print('initial')
                g.save()
                group.append(g.pk)
            else:
                try:
                    if (int(label[i - 1][-1:]) == int(label[i][-1:]) - 1) or (
                                int(label[i - 1][-1:]) == int(label[i][-1:]) + 9):
                        group.append(g.pk)
                        print('same, do nothing')
                    else:
                        g = Groups(survey=s, colour='FF0000', type='PL', single_point=False)
                        g.save()
                        group.append(g.pk)
                        print('change')
                except ValueError:
                    g = Groups(survey=s, colour='FF0000', type='PL', single_point=False)
                    g.save()
                    group.append(g.pk)
                    print('change')

            if system == 'NE':
                OSGBe[i], OSGBn[i], OSGBh[i] = points[i][0], points[i][1], points[i][2]
                input_type.append('OSGB')
                ETRS89lat[i], ETRS89lng[i], ETRS89h[i] = webgui_convert(points[i][0], points[i][1], points[i][2],
                                                                        convert)
            elif system == 'DD':
                ETRS89lat[i], ETRS89lng[i], ETRS89h[i] = points[i][0], points[i][1], points[i][2]
                input_type.append('ETRS89')
                OSGBe[i], OSGBn[i], OSGBh[i] = webgui_reverse(points[i][0], points[i][1], points[i][2])
        groupset = set(group)
        print(groupset)
        for groupcheck in groupset:
            if group.count(groupcheck) == 1:
                g = Groups.objects.get(pk=groupcheck)
                g.single_point = True
                g.save()

        data = zip(label, OSGBe, OSGBn, OSGBh, ETRS89lat, ETRS89lng, ETRS89h, group, input_type)
        print(data)
    else:
        OSGBe = numpy.zeros(1)
        OSGBn = numpy.zeros(1)
        OSGBh = numpy.zeros(1)
        ETRS89lat = numpy.zeros(1)
        ETRS89lng = numpy.zeros(1)
        ETRS89h = numpy.zeros(1)
        input_type = []
        group = []
        label = 'Single Point'
        g = Groups(survey=s, colour='FF0000', type='PL', single_point=True)
        print('single')
        g.save()
        group.append(g.pk)
        if system == 'NE':

            OSGBe[0], OSGBn[0], OSGBh[0] = float(request.POST['east']), float(request.POST['north']), float(request.POST['height'])
            input_type.append('OSGB')
            ETRS89lat[0], ETRS89lng[0], ETRS89h[0] = webgui_convert(float(request.POST['east']),
                                                                    float(request.POST['north']),
                                                                    float(request.POST['height']), convert)

        elif system == 'DMS':
            input_type.append('ETRS89')
            if float(request.POST['latd']) > 0:
                ETRS89lat[0] = float(request.POST['latd']) + (float(request.POST['latm']) / 60) + (
                    float(request.POST['lats']) / 3600)

            else:
                ETRS89lat[0] = float(request.POST['latd']) - (float(request.POST['latm']) / 60) - (
                    float(request.POST['lats']) / 3600)
            if float(request.POST['lngd']) > 0:
                ETRS89lng[0] = float(request.POST['lngd']) + (float(request.POST['lngm']) / 60) + (
                    float(request.POST['lngs']) / 3600)
            else:
                ETRS89lng[0] = float(request.POST['lngd']) - (float(request.POST['lngm']) / 60) - (
                    float(request.POST['lngs']) / 3600)

            ETRS89h[0] = float(request.POST['height'])
            OSGBe[0], OSGBn[0], OSGBh[0] = webgui_reverse(ETRS89lat[0], ETRS89lng[0], ETRS89h[0])

        else:
            input_type.append('ETRS89')
            ETRS89lat[0] = float(request.POST['latdd'])
            ETRS89lng[0] = float(request.POST['lngdd'])
            ETRS89h[0] = float(request.POST['height'])
            OSGBe[0], OSGBn[0], OSGBh[0] = webgui_reverse(ETRS89lat[0], ETRS89lng[0], ETRS89h[0])

        data = zip(label, OSGBe, OSGBn, OSGBh, ETRS89lat, ETRS89lng, ETRS89h, group, input_type)
        print(data)

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


def kml(request, survey_id):
    try:
        survey = Survey.objects.get(pk=survey_id)
        points = Points.objects.filter(survey=survey)
        groups = Groups.objects.filter(survey=survey)
        for group in groups:
            group.colour = group.colour[4:6] + group.colour[2:4] + group.colour[0:2]
        file = render(request, 'converter/survey.kml', {'survey': survey, 'points': points, 'groups': groups})
        response = HttpResponse(file, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Length'] = len(response.content)
        response['Content-Disposition'] = 'attachment; filename=%s.kml' % survey.name

    except Survey.DoesNotExist:
        raise Http404
    return response


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
