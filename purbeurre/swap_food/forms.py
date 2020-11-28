from django import forms

class SearchForm(forms.Form):
    aliment_name = forms.CharField(label='Your name', max_length=100)