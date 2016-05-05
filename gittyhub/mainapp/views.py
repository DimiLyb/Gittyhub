from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import NameForm
from .loginform import loginf
from .repo import getrepo, getjson, getfile, getgit, gitlog, logjson
import json

#import urllib.request, json, os, requests, redis 
#from http import cookies
#from http.client import HTTPSConnection
#from base64 import b64encode

def index(request): 
    mylist = []
    errorm = ["Please log in to get more requests form the github API","alert alert-info"]
    if 'mylist' in request.session:
        mylist = request.session['mylist']
    if 'errorm' in request.session:
        errorm = request.session['errorm']
    form = NameForm()
    log = loginf()
    if request.method == 'POST':
        if 'clean' in request.POST: #remove all urls from curent list
            mylist = []
            request.session['mylist'] = mylist
            return render(request, 'repo.html', {'form': form, 'mylist': mylist, 'log': log, 'err': errorm})
         
        if 'add' in request.POST: #add url to list
            form = NameForm(request.POST)
            if form.is_valid():
                
                mylist.append( form.cleaned_data['getjson'] )
                request.session['mylist'] = mylist
                form = NameForm()
                return render(request, 'repo.html', {'form': form, 'mylist': mylist, 'log': log, 'err': errorm})
                
        if 'submit' in request.POST: #Login 
            log = loginf(request.POST)
            if log.is_valid():
                request.session['login'] = log.cleaned_data['login']
                request.session['passw'] = log.cleaned_data['passw']
                r = getrepo("https://api.github.com/", request)
                errorm = ["",""]
                if 'message' in r():
                    errorm[0] = "Bad login" 
                    errorm[1] = "alert alert-danger"
                    del request.session['login']
                    del request.session['passw']
                else:
                    errorm[0] = "Your loged in" 
                    errorm[1] = "alert alert-success"
                request.session['errorm'] = errorm
                return render(request, 'repo.html', {'form': form, 'mylist': mylist, 'log': log, 'err': errorm})
        if 'logout' in request.POST: #logout
            if 'login' in request.session:
                del request.session['login']
            if 'passw' in request.session:  
                del request.session['passw']
            errorm = ["Please log in to get more requests form the github API","alert alert-info"]
            return render(request, 'repo.html', {'form': form, 'mylist': mylist, 'log': log, 'err': errorm})
            
        if 'pop' in request.POST:
            if mylist:
                del mylist[-1]
                #mylist.pop()
            return render(request, 'repo.html', {'form': form, 'mylist': mylist, 'log': log, 'err': errorm})
            
        if 'getrepo' in request.POST: # load repo list
            if mylist:
                r = []
                for item in mylist:
                    r.append(getrepo(item, request))
                    
                #r = getrepo(mylist[0], request)
                return render(request, 'anwser.html', {'test': r })
            else:
                 return render(request, 'repo.html', {'form': form, 'mylist': mylist, 'log': log, 'err': errorm})
        if 'rest' in request.POST:
            request.session.flush()
            mylist = []
            errorm = ["Please log in to get more requests form the github API","alert alert-info"]
            return render(request, 'repo.html', {'form': form, 'mylist': mylist, 'log': log, 'err': errorm})
    errorm = ["Please log in to get more requests form the github API","alert alert-info"]
    return render(request, 'repo.html', {'form': form, 'mylist': mylist, 'log': log, 'err': errorm})
    
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

def jsonMC(request, owner, repo, fork):
    lol = logjson(request, owner, repo, fork)
    return render(request, 'lol.html', {'lol': lol})
    

#Markesout stuff
    #return HttpResponse("Hello, world. You're at the GittyHub index.")
    #r = r.decode("utf-8")
    #r = json.loads(r) 
    #mylist.append( form.cleaned_data['getjson'] )
    #request.session['mylist'] = mylist 
    #re = redis.StrictRedis(host='localhost', port=6379, db=0)
    #commit = getrepo(r["commits_url"])
    #return render(request, 'repo.html', {'form': form, 'mylist': mylist})
    #return HttpResponse(getrepo(form.cleaned_data['getjson'])) 

#testing stuff
def thanks(request):
    
    #mylist = ["een","twee"]
    
    
    #bla = request.session.get('fav_color')
    #url = 'https://api.github.com/repos/' + 'DimiLyb'  + '/' + 'Gittyhub' + '/branches/' + 'master'
    #getsha = getrepo(url, request)
    #return HttpResponse(getsha)
    #return HttpResponse(getrepo("https://api.github.com/authorizations", request))
    #return HttpResponse(gitlog("Gittyhub_DimiLyb")) 
    #lol = gitlog("octokit.rb_octokit")
    lol = logjson(request, 'DimiLyb', 'Gittyhub', 'master')
    #return HttpResponse(lol) 
    return render(request, 'lol.html', {'lol': lol})
    #return HttpResponse(os.path.dirname(os.path.abspath(__file__)))

"""
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
"""
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
    if request.method == 'POST':
        form = loginf(request.POST)
        if form.is_valid():
            request.session['login'] = form.cleaned_data['login']
            request.session['passw'] = form.cleaned_data['passw']
            #r = getrepo(form.cleaned_data['getjson'], request)
            #re = redis.StrictRedis(host='localhost', port=6379, db=0)
            #commit = getrepo(r["commits_url"])
            return render(request, 'login.html', {'test': r })
            #return HttpResponse(getrepo(form.cleaned_data['getjson']))
    else:
        form = loginf()
    return render(request, 'login.html', {'form': form})
"""

    #https://github.com/DimiLyb/Gittyhub.git
    
    