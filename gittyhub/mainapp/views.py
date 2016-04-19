from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import urllib.request, json, redis, os

from http.client import HTTPSConnection
from base64 import b64encode

from .forms import NameForm #loginform
from .repo import getrepo, getjson, getfile
from .loginform import loginf



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
        
    return render(request, 'repo.html', {'form': form})

def download(request, owner, repo, fork):
    url = "https://github.com/" + owner + "/" + repo + "/archive/" + fork + ".zip" 
    name = repo + "_" + owner + ".zip"
    getfile(url, name)
    return render(request, 'download.html', {'repo': repo, 'owner': owner, 'fork': fork})
    
    
def commit(request, owner, repo):
    urlcommit = "https://api.github.com/repos/" + owner + "/" + repo + "/commits"
    c = getrepo(urlcommit)
    return render(request, 'commit.html', {'commit': c, 'owner': owner, 'repo': repo })

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
    
def login(request): 
            #c = HTTPSConnection("api.github.com")
            #user = ""
            #passw= ""
            #logi = bytes(user + ':' + passw, 'utf-8')
            #userAndPass = b64encode(logi).decode("ascii")
            #headers = { 'Authorization' : 'Basic %s' %  userAndPass, 'User-Agent': user }
            #c.request('GET', '/', headers=headers)
            #res = c.getresponse()
            #data = res.read()  
            #return HttpResponse(data)
            
            userName = ""
            passWord  = ""
            top_level_url = "https://api.github.com/orgs/octokit/repos"
    
            # create an authorization handler
            p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            p.add_password(None, top_level_url, userName, passWord);
            auth_handler = urllib.request.HTTPBasicAuthHandler(p)
            opener = urllib.request.build_opener(auth_handler)
            urllib.request.install_opener(opener)
            result = opener.open(top_level_url)
            messages = result.read()
            #return messages
            return HttpResponse(messages)