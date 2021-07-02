from django import forms
from django.forms import ModelForm
from public_site.models import *
from django.db import connection
from django.utils.safestring import mark_safe


class HorizontalRadioSelect(forms.RadioSelect):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs, choices)

    # Non funziona
    """
    def render(self, name, value, attrs=None, renderer=None):
        html_str = super().render(name, value, attrs=attrs, renderer=renderer)
        return mark_safe('<div class="form-check form-check-inline">\n{}\n</div>'.format(html_str))
    """



    def render(self, name, value, attrs=None, renderer=None):
        # Render the widget as an HTML string.
        context = self.get_context(name, value, attrs)
        html_str = ''
        id = context.get('widget', {}).get('attrs', {}).get('id', None)
        #html_str += '<ul'
        #if id: html_str += ' id="' + id + '"'
        #if context.get('widget', {}).get('attrs', {}).get('class', None):
        #    html_str += ' class="' + context['widget']['attrs']['class']
        #html_str += '>'
        # noi iniziamo a scrivere dopo un <td>
        #html_str += '    </td>'
        for group, options, index in context.get('widget', {}).get('optgroups', []):
            #if group:
            #    html_str += '<li>' + group + '<ul'
            #    if id: html_str += ' id="' + id + '_' + index + '"'
            #    html_str += '>'
            for option in options:
                if option.get('wrap_label', False):
                    html_str += '<span><label'
                    #html_str += '&nbsp&nbsp&nbsp<span><label'
                    if option.get('attrs', {}).get('id', None): html_str += ' for="' + option['attrs']['id'] + '"'
                    html_str += '>'

                #{% include "django/forms/widgets/input.html" %}
                html_str += '<input type="' + option.get('type', '') + '" name="' + option.get('name', '') + '"'
                if option.get('value', None) != None: html_str += ' value="' + str(option['value']) + '"'
                #{% include "django/forms/widgets/attrs.html" %}
                for name, value in option.get('attrs', {}).get('items', []):
                    if value is not False: html_str += ' ' + name
                    if value is not True: html_str += '="' + str(value) + '"'

                html_str += '>'

                if option.get('wrap_label', False): html_str += ' ' + option['label'] + '&nbsp;&nbsp;&nbsp;</label>'
                html_str += '</span>'
            #if group: html_str += '</ul></li>'
        #html_str += '</ul>'
        return mark_safe(html_str)



class AnnoUniForm(forms.Form):
    laurea_aa = forms.ChoiceField(label='Anno Accademico', choices=[], widget=forms.Select(attrs={'class': 'custom-select mb-2'}), required=False)
    uni_nome = forms.ChoiceField(label='Università', choices=[], widget=forms.Select(attrs={'class': 'custom-select mb-2'}), required=False)

    def __init__(self, *args, **kwargs):
        user_details = kwargs.pop('user_details', None)
        super(AnnoUniForm, self).__init__(*args, **kwargs)
        if user_details:
            self.fields['uni_nome'].choices = user_details['uni_nome']
            self.fields['laurea_aa'].choices = user_details['laurea_aa']

# DA NON FARE MAI: 'pattern':r'^\d{13}$' o qualsiasi altra condizione perché se la condizione viene violata non parte il POST !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#'autocomplete': 'off', Quando si torna indietro scompare l'ean inserito
class PublisherForm(forms.Form):
    a_a = forms.ChoiceField(label='A. A.', choices=[], widget=forms.Select(attrs={'class': 'custom-select mb-2'}), required=False)
    uni_cod = forms.ChoiceField(label='Università', choices=[], widget=forms.Select(attrs={'class': 'custom-select mb-2'}), required=False)
    ean = forms.CharField(label='ISBN-13', widget=forms.TextInput(attrs={'size': '20', 'class':'form-control', 'title':'Inserire 13 cifre '}),
                            required = False, initial='')

    autore = forms.CharField(label='Autore/i', widget=forms.TextInput(attrs={'size': '50', 'class': "form-control"}), required=False,
                            initial='')
    titolo = forms.CharField(label='Titolo', widget=forms.TextInput(attrs={'size': '50', 'class': "form-control"}), required=False,
                            initial='')
    editore = forms.CharField(label='Editore', widget=forms.TextInput(attrs={'size': '50', 'class': "form-control"}), required=False,
                            initial='')

    tipi_lauree = [('0', 'Tutte'),('L', 'Triennale'),('LM', 'Magistrale'),('LMCU', 'Magistrale a ciclo unico')]
    tipo_laurea = forms.ChoiceField(label='Tipo laurea', choices=tipi_lauree, widget=HorizontalRadioSelect(), required=False)
    laurea = forms.CharField(label='Laurea', widget=forms.TextInput(attrs={'size': '50', 'class': "form-control"}), required=False,
                            initial='')
    corso = forms.CharField(label='Corso', widget=forms.TextInput(attrs={'size': '50', 'class': "form-control"}), required=False,
                            initial='')
    area_cod = forms.ChoiceField(label='Area', choices=[], widget=forms.Select(attrs={'class': 'custom-select mb-2'}), required=False)
    ssd_cod = forms.ChoiceField(label='SSD', choices=[], widget=forms.Select(attrs={'class': 'custom-select mb-2'}), required=False)
    opzioni_ord = [('1', 'Titolo libro, uni'),('2', 'Classe di laurea, anno di corso, ssd')]
    opzione_ord = forms.ChoiceField(label='Ordina per:', choices=opzioni_ord, widget=HorizontalRadioSelect(), required=False)


    def __init__(self, *args, **kwargs):
        a_a_choices = kwargs.pop('a_a')
        uni_cod_choices = kwargs.pop('uni_cod')
        #senza if la pagina mantiene le scelte effettuate
        #però va in errore se si istanzia la form in vista di un is_valid()
        #if len(kwargs.get('area_cod', [])) > 0:
        area_choices = kwargs.pop('area_cod')
        #if len(kwargs.get('ssd_cod', [])) > 0:
        ssd_choices = kwargs.pop('ssd_cod')
        hide_ord = kwargs.pop('hide_ord')
        super(PublisherForm, self).__init__(*args, **kwargs)
        if hide_ord:
            self.fields['opzione_ord'].choices = []
            self.fields['opzione_ord'].label = ''
        self.fields['a_a'].choices = a_a_choices
        self.fields['uni_cod'].choices = uni_cod_choices
        self.fields['area_cod'].choices = area_choices
        self.fields['ssd_cod'].choices = ssd_choices

class MiddleSize_Form(forms.Form):
    a_a = forms.ChoiceField(label='A. A.', choices=[], widget=forms.Select(attrs={'class': 'custom-select mb-2'}), required=False)
    uni_cod = forms.ChoiceField(label='Università', choices=[], widget=forms.Select(attrs={'class': 'custom-select mb-2'}), required=False)
    tipi_lauree = [('0', 'Tutte'),('L', 'Triennale'),('LM', 'Magistrale'),('LMCU', 'Magistrale a ciclo unico')]
    tipo_laurea = forms.ChoiceField(label='Tipo laurea', choices=tipi_lauree, widget=HorizontalRadioSelect(), required=False)
    laurea = forms.CharField(label='Laurea', widget=forms.TextInput(attrs={'size': '50', 'class': "form-control"}), required=False,
                            initial='')
    corso = forms.CharField(label='Corso', widget=forms.TextInput(attrs={'size': '50', 'class': "form-control"}), required=False,
                            initial='')
    area_cod = forms.ChoiceField(label='Area', choices=[], widget=forms.Select(attrs={'class': 'custom-select mb-2'}), required=False)
    ssd_cod = forms.ChoiceField(label='SSD', choices=[], widget=forms.Select(attrs={'class': 'custom-select mb-2'}), required=False)

    def __init__(self, *args, **kwargs):
        form_func = None
        if kwargs.get('form_func'):
            form_func = kwargs.pop('form_func')
        a_a_choices = kwargs.pop('a_a')
        uni_choices = kwargs.pop('uni_cod')
        #senza if la pagina mantiene le scelte effettuate
        #però va in errore se si istanzia la form in vista di un is_valid()
        #if len(kwargs.get('area_cod', [])) > 0:
        area_choices = kwargs.pop('area_cod')
        #if len(kwargs.get('ssd_cod', [])) > 0:
        ssd_choices = kwargs.pop('ssd_cod')
        super(MiddleSize_Form, self).__init__(*args, **kwargs)
        if form_func == 'rankings':
            self.fields.pop('uni_cod')
        else:
            self.fields['uni_cod'].choices = uni_choices
        self.fields['a_a'].choices = a_a_choices
        self.fields['area_cod'].choices = area_choices
        self.fields['ssd_cod'].choices = ssd_choices
