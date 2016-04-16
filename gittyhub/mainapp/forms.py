from django import forms

class NameForm(forms.Form):
    getjson = forms.CharField(label='repo', max_length=100)