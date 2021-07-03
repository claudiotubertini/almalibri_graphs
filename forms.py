from django import forms
from django.forms import ModelForm
from public_site.models import *
from django.db import connection
from django.utils.safestring import mark_safe


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()