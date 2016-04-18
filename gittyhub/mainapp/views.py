from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import urllib.request, json, redis, os

from .forms import NameForm
from .repo import getrepo, getjson, getfile



def index(request):
    #return HttpResponse("Hello, world. You're at the GittyHub index.")
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            r = getrepo(form.cleaned_data['getjson'])
            #re = redis.StrictRedis(host='localhost', port=6379, db=0)
            #commit = getrepo(r["commits_url"])
            return render(request, 'anwser.html', {'test': r })
            #return HttpResponse(getrepo(form.cleaned_data['getjson']))
    else:
        form = NameForm()
        
    return render(request, 'repo.html', {'form': form , 'test': "lol"})

def download(request, owner, repo, fork):
    url = "https://github.com/" + owner + "/" + repo + "/archive/" + fork + ".zip" 
    name = repo + "_" + owner + ".zip"
    getfile(url, name)
    return render(request, 'download.html', {'repo': repo, 'owner': owner, 'fork': fork})
    
    
def commit(request, owner, repo):
    urlcommit = "https://api.github.com/repos/" + owner + "/" + repo + "/commits"
    c = getrepo(urlcommit)
    return render(request, 'commit.html', {'commit': c })



#testing stuff
def thanks(request):
    #return HttpResponse(getrepo("https://api.github.com/repos/octokit/octokit.rb/commits"))
    return HttpResponse(os.path.dirname(os.path.abspath(__file__)))

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponse(getrepo(form.cleaned_data['getjson']))
    else:
        form = NameForm()

    return render(request, 'repo.html', {'form': form})