# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'converter/index.html')

def map(request):
    input = request.POST['coordinate']
    return render(request, 'converter/map.html')

