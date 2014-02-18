from django.conf.urls import patterns, url

from converter import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^process/$', views.process, name='process'),
    url(r'^(?P<survey_id>\d+)/review/$', views.review, name='review'),
    url(r'^(?P<survey_id>\d+)/gmaps/$', views.gmap, name='gmap'),
    url(r'^(?P<survey_id>\d+)/bmaps/$', views.bmap, name='bmap'),
    url(r'^(?P<survey_id>\d+)/ostreetmap/$', views.ostreetmap, name='ostreetmap'),
    url(r'^(?P<survey_id>\d+)/OSmap/$', views.OSmap, name='OSmap'),
    url(r'^(?P<survey_id>\d+)/kml/$', views.kml, name='kml'),
    url(r'^update/$', views.update_group, name='update_group')
)