from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import NameForm
from .repo import getrepo, getjson, getfile, getgit

#import urllib.request, json, os, requests, redis 
#from http import cookies
#from http.client import HTTPSConnection
#from base64 import b64encode
from .loginform import loginf
#from .form2 import MyForm


def index(request):
    #return HttpResponse("Hello, world. You're at the GittyHub index.")
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.session['login'] = form.cleaned_data['login']
            request.session['passw'] = form.cleaned_data['passw']
            r = getrepo(form.cleaned_data['getjson'], request)
            #re = redis.StrictRedis(host='localhost', port=6379, db=0)
            #commit = getrepo(r["commits_url"])
            return render(request, 'anwser.html', {'test': r })
            #return HttpResponse(getrepo(form.cleaned_data['getjson']))
    else:
        form = NameForm()
    return render(request, 'repo.html', {'form': form})
    
       
def setrepo(request):
    #return HttpResponse("Hello, world. You're at the GittyHub index.")
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            
            r = getrepo(form.cleaned_data['getjson'], request)
            return render(request, 'anwser.html', {'test': r })
            
            #re = redis.StrictRedis(host='localhost', port=6379, db=0)
            #commit = getrepo(r["commits_url"])
            #return HttpResponse(getrepo(form.cleaned_data['getjson']))
    else:
        form = NameForm()
    return render(request, 'repo.html', {'form': form})
    

def download(request, owner, repo, fork):
    #return render(request, 'holdOn.html', {'repo': repo, 'owner': owner, 'fork': fork})
    url = "https://github.com/" + owner + "/" + repo + "/archive/" + fork + ".zip" 
    name = repo + "_" + owner + ".zip"
    getfile(url, name)
    return render(request, 'download.html', {'repo': repo, 'owner': owner, 'fork': fork})
    
def downloadgit(request, owner, repo):
    url = "https://github.com/" + owner + "/" + repo + ".git" 
    name = repo + "_" + owner
    messages = getgit(url, name, owner, repo)
    return render(request, 'downloadgit.html', {'mess': messages})    

def commit(request, owner, repo):
    urlcommit = "https://api.github.com/repos/" + owner + "/" + repo + "/commits"
    c = getrepo(urlcommit, request)
    return render(request, 'commit.html', {'commit': c, 'owner': owner, 'repo': repo })






#testing stuff
def thanks(request):
    bla = request.session.get('fav_color')
    return HttpResponse(bla)
    #return HttpResponse(getrepo("https://api.github.com/orgs/octokit/repos"))  
    #return HttpResponse(os.path.dirname(os.path.abspath(__file__)))
"""
def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponse(getrepo(form.cleaned_data['getjson']))
    else:
        form = NameForm()

    return render(request, 'repo.html', {'form': form})
"""
"""    
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
"""
"""           
def myview(request):
    if request.method == 'POST':
        form = MyForm(request.POST, extra=request.POST.get('extra_field_count'))
        if form.is_valid():
            return HttpResponse("oke")
    else:
        form = MyForm()
    return render(request, "template.html", { 'form': form })
"""

    #https://github.com/DimiLyb/Gittyhub.git
    