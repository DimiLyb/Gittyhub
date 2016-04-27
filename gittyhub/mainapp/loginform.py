from django import forms
 
class loginf(forms.Form):
    login = forms.CharField(label='Github username', max_length=100)
    passw = forms.CharField(max_length=100, widget=forms.PasswordInput,label='Github Password')