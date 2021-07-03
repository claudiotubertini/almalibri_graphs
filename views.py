
from django.shortcuts import render, redirect, Http404
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
import datetime
from public_site.forms import *
from public_site.templatetags.new_tags import academicyear
import public_site.queries
import public_site.confirmed_adoptions
import public_site.streamcsv
from django.contrib.auth import authenticate, login
from django.db import connection
from django.core import serializers
import json


def graphs(request):
    return render(request, 'graph_D3_2.html', {})

### oppure ###

def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})

def population_chart(request):
    data = public_site.queries.search_test()
    # data = serializers.serialize('json', data, fields=('publisher', 'count'))
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