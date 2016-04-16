from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import urllib.request, json

from .forms import NameForm
from .repo import getrepo, getjson

def index(request):
    #return HttpResponse("Hello, world. You're at the GittyHub index.")
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            r = getrepo(form.cleaned_data['getjson'])
            #data = getjson(r)
            return render(request, 'anwser.html', {'form': form, 'test': r})
            #return HttpResponse(getrepo(form.cleaned_data['getjson']))
    else:
        form = NameForm()
        
    return render(request, 'repo.html', {'form': form , 'test': "lol"})







#testing stuff
def thanks(request):
    return HttpResponse(getrepo("https://api.github.com/users/DimiLyb"))

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponse(getrepo(form.cleaned_data['getjson']))
    else:
        form = NameForm()

    return render(request, 'repo.html', {'form': form})