from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import urllib.request, json, redis

from .forms import NameForm
from .repo import getrepo, getjson, getfile



def index(request):
    #return HttpResponse("Hello, world. You're at the GittyHub index.")
    x = []
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            r = getrepo(form.cleaned_data['getjson'])
            re = redis.StrictRedis(host='localhost', port=6379, db=0)
            
            #commit = getrepo(r["commits_url"])
            for item in r:
              i = 0
              urlcommit = "https://api.github.com/repos/" + r[i]["full_name"] + "/commits"
              commit = getrepo(urlcommit)
              x.append(commit)
              i = i + 1
            return render(request, 'anwser.html', {'test': r, 'commit': x })
            #return HttpResponse(getrepo(form.cleaned_data['getjson']))
    else:
        form = NameForm()
        
    return render(request, 'repo.html', {'form': form , 'test': "lol"})

def download(request, owner, repo, fork):
    url = "https://github.com/" + owner + "/" + repo + "/archive/" + fork + ".zip" 
    name = repo + "_" + owner + ".zip"
    getfile(url, name)
    return render(request, 'download.html', {'repo': repo, 'owner': owner, 'fork': fork})
    #getfile()
    





#testing stuff
def thanks(request):
    return HttpResponse(getrepo("https://api.github.com/repos/octokit/octokit.rb/commits"))

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponse(getrepo(form.cleaned_data['getjson']))
    else:
        form = NameForm()

    return render(request, 'repo.html', {'form': form})