from django import forms

class NameForm(forms.Form):
    getjson = forms.CharField(label='Add user repo: https://api.github.com/orgs/(user)/repos  ', max_length=100)
    
