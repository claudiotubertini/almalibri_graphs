
from django.shortcuts import render, redirect, Http404
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.http import JsonResponse
import datetime
from graphs.forms import UploadFileForm
import public_site.queries
import public_site.confirmed_adoptions
import public_site.streamcsv
from django.contrib.auth import authenticate, login
from django.db import connection
from django.core import serializers
import json, csv
import pandas as pd

def handle_uploaded_file(f):
    result = []
    with open(f, newline='') as csvfile:
         reader = csv.DictReader(csvfile, delimiter=';')
         for row in reader:
            result.append(row)
    return result
    # df = pd.read_csv (f)
    # df.to_json (r'Path where the new JSON file will be stored\New File Name.json')
    # with open('some/file/name.txt', 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            data = handle_uploaded_file(request.FILES['file'])
    else:
        form = UploadFileForm()
    #return JsonResponse(data, safe=False)
    return render(request, 'upload.html', {'form': form})


def graphs(request):
    return render(request, 'graph_D3_A.html')

### oppure ###

def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})

def population_chart(request):
    #data = public_site.queries.search_test()
    # data = serializers.serialize('json', data, fields=('publisher', 'count'))
    result = upload_file(request)
    result = []
    keys = ('publisher','count')
    for row in data:
        result.append(dict(zip(keys,row)))
    #json_data = json.dumps(result)
    return JsonResponse(result, safe=False)
    # publisher = []
    # count = []
    # for entry in data:
    #     publisher.append(entry[0])
    #     count.append(entry[1])
    
    # return JsonResponse(data={
    #     'publisher': publisher,
    #     'count': count,
    # })

## oppure ###
def pivot_data(request):
    data = public_site.queries.search_test()
    # dataset = Order.objects.all()
    data = serializers.serialize('json', data)
    return JsonResponse(data, safe=False)