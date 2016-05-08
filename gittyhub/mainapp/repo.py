#from django.shortcuts import render
#from django.http import HttpResponse, HttpResponseRedirect
#from django import forms
#from http import cookies
#from http.client import HTTPSConnection
#from base64 import b64encode

import json, zipfile, git, sys, os.path, requests, shutil, platform
#os, base64, urllib.response, urllib.parse, stat, urllib.request, urllib,
from collections import Counter
from gittyhub import settings 

#req = urllib.request

def getrepo(valu , request):
    #with urllib.request.urlopen(valu, auth=requests.auth.HTTPBasicAuth('', '')) as url: s = url.read()
    #r = getjson(s)
    a = ""
    if 'login' in request.session:
        login = request.session.get('login')
        passw = request.session.get('passw')
        r = requests.get(valu, auth=(login, passw))
        a = r.json
    else:
        r = requests.get(valu)
        a = r.json
    return a
    
    # byte to json
def getjson(valu):
    valu = valu.decode("utf-8")
    data = json.loads(valu)
    return data
    
def getfile(url, file_name):
    plat = platform.system()
    filename = ""
    filename = os.path.join(settings.BASE_DIR + '/repos/zip_download/', file_name)       
    file = requests.get(url, stream=True)
    dump = file.raw
    with open(filename, 'wb') as out_file:shutil.copyfileobj(dump, out_file)
    getunzip(file_name)
    del dump
  
def getunzip(file_name):
    plat = platform.system()
    filename = ""
    with zipfile.ZipFile(settings.BASE_DIR + '/repos/zip_download/' + file_name, "r") as z: z.extractall(settings.BASE_DIR + '/repos/zip_download/')
        #settings.BASE_DIR + "/repos/zip_download/"
    #with zipfile.ZipFile(r'C:\ap\repos\\' + file_name, "r") as z: z.extractall(r'C:\ap\repos\\')
    
def getgit(url, file_name, owner, rep):
    
    DIR_NAME = settings.BASE_DIR + "/repos/" +  file_name
    REMOTE_URL = url
    message = ["",""]
    if os.path.isdir(DIR_NAME):
            #g = git.cmd.Git(git_dir)
            #g.pull()
            #shutil.rmtree(DIR_NAME, onerror=set_rw)
            message[0] = "Can't download " + owner + "\'s project " + rep + " with git it already exists. Please remove the old version ."
            message[1] = "alert alert-danger"
    else:
            os.mkdir(DIR_NAME)
            repo = git.Repo.init(DIR_NAME)
            origin = repo.create_remote('origin',REMOTE_URL)
            origin.fetch()
            origin.pull(origin.refs[0].remote_head)
            message[0] = "Download has started from " + owner+ "\'s project " + rep + " with git."
            message[1] = "alert alert-success"
    return message
    #https://github.com/octokit/octokit.rb.git
    #https://api.github.com/repos/DimiLyb/Gittyhub/branches/master
    #https://api.github.com/repos/DimiLyb/Gittyhub/git/commits/9a6872c89ef865d793e5e439a6fed98e40700f93
    
def set_rw(operation, name, exc):
    os.chmod(name, stat.S_IWRITE)
    return True

    #shutil.rmtree('path', onerror=set_rw)
    
def gitlog(file_name):
    g = git.Git(settings.BASE_DIR + "/repos/" +  file_name) 
    loginfo = g.log('--pretty=tformat:','--numstat')
    loginfo = loginfo.replace('-	-' , '0	0')
    loginfo = loginfo.split()
    bla = len(loginfo)
    num = -1
    logbox = []
    logbox2 = []
    while (num <= len(loginfo) - 2):
        temp = [0,0,'']
        temp[0] = loginfo[num + 1]
        temp[1] = loginfo[num + 2]
        temp[2] = loginfo[num + 3]
        logbox.append(temp)
        if (temp[1] >= 0):
            if (temp[2] >= 0):
                logbox2.append(temp[2])
        num = num + 3
    myDict = Counter(logbox2).most_common(10)
    #loginfo = g.rev_list('--objects', '--all')
    return myDict
    
def logjson(request, user, repo, fork):
    url = 'https://api.github.com/repos/' + user  + '/' + repo + '/branches/' + fork
    getsha = getrepo(url, request)
    #test = getsha()['commit']
    filesurl = 'https://api.github.com/repos/' + user  + '/' + repo + '/commits/' + getsha()['commit']['sha']
    return logloop(request, [] , filesurl)
    
def logloop(request, listjson, url):
    file = getrepo(url, request)
    #test = listjson
    for item in file()['files']:
        #listjson.append("bla")
        listjson.append(item['filename'])
    par = file()['parents']
    if  par:
        #test  = file()['parents'][0]['sha']
        #newurl = 'https://api.github.com/repos/' + user  + '/' + repo + '/commits/' + file()['parents'][0]['sha']
        newurl = file()['parents'][0]['url']
        logloop(request, listjson, newurl)
        
    else:
        myDict = Counter(listjson).most_common(10)
        return myDict
    myDict = Counter(listjson).most_common(10)
    return myDict

def commitjson(request, user, repo, fork):
    url = 'https://api.github.com/repos/' + user  + '/' + repo + '/branches/' + fork
    getsha = getrepo(url, request)
    #test = getsha()['commit']
    filesurl = 'https://api.github.com/repos/' + user  + '/' + repo + '/commits/' + getsha()['commit']['sha']
    return commitloop(request, [] , filesurl)

def commitloop(request, listjson, url):
    file = getrepo(url, request)
    #test = listjson
    listjson.append(file)
    par = file()['parents']
    if  par:
        #test  = file()['parents'][0]['sha']
        #newurl = 'https://api.github.com/repos/' + user  + '/' + repo + '/commits/' + file()['parents'][0]['sha']
        newurl = file()['parents'][0]['url']
        commitloop(request, listjson, newurl)
        
    else:
        return listjson
    return listjson
    
def mylistcheck(mylist):
    for i in xrange(len(mylist)):
        varsplit = mylist[i].split('/')
        if (len(varsplit) == 5):
            if (varsplit[2] != "api.github.com" ):
                mylist[i] = "https://api.github.com/repos/" + varsplit[3] + "/" + varsplit[4].replace('.git','')
    return mylist
    
    