from django import forms 

class NameForm(forms.Form):
    getjson = forms.URLField(label='Add user repo: https://api.github.com/repos/{users}/{repo}  ', max_length=200, required=False, initial='')