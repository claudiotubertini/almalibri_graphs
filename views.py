
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


def graphs(request):
    return render(request, 'graph_D3.html')
    


def population_chart(request):
    data = public_site.queries.search_test()
    
    publisher = []
    count = []
    for entry in data:
        publisher.append(entry[0])
        count.append(entry[1])
    
    return JsonResponse(data={
        'publisher': publisher,
        'count': count,
    })
