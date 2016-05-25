#from django.shortcuts import render
#from django.http import HttpResponse, HttpResponseRedirect
#from django import forms
#from http import cookies
#from http.client import HTTPSConnection
#from base64 import b64encode

import json, zipfile, sys, os.path, requests, shutil, platform
#os, base64, urllib.response, urllib.parse, stat, urllib.request, urllib, git,
from collections import Counter
from gittyhub import settings 

def getrepo(valu , request):
    a = ""
    try:
        if 'login' in request.session:
            login = request.session.get('login')
            passw = request.session.get('passw')
            r = requests.get(valu, auth=(login, passw))
            a = r.json
        else:
            r = requests.get(valu)
            a = r.json
    except:
            a = ["{'nope': nada }"]
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
    
def set_rw(operation, name, exc):
    os.chmod(name, stat.S_IWRITE)
    return True
    
def logjson(request, user, repo, fork):
    url = 'https://api.github.com/repos/' + user  + '/' + repo + '/branches/' + fork
    getsha = getrepo(url, request)
    filesurl = 'https://api.github.com/repos/' + user  + '/' + repo + '/commits/' + getsha()['commit']['sha']
    return logloop(request, [] , filesurl)
    
def logloop(request, listjson, url):
    file = getrepo(url, request)
    for item in file()['files']:
        listjson.append(item['filename'])
    par = file()['parents']
    if  par:
        newurl = file()['parents'][0]['url']
        logloop(request, listjson, newurl)
        
    else:
        myDict = Counter(listjson).most_common(10)
        return myDict
    myDict = Counter(listjson).most_common(10)
    comlist = json.dumps(myDict)
    comlist = getjson(comlist)
    return comlist

def commitjson(request, user, repo, fork):
    url = 'https://api.github.com/repos/' + user  + '/' + repo + '/branches/' + fork
    getsha = getrepo(url, request)
    filesurl = 'https://api.github.com/repos/' + user  + '/' + repo + '/commits/' + getsha()['commit']['sha']
    return commitloop(request, [] , filesurl, 1)
    
def commitjsonnext(request, user, repo, sha):
    filesurl = 'https://api.github.com/repos/' + user  + '/' + repo + '/commits/' + sha
    return commitloop(request, [] , filesurl, 1)

def commitloop(request, listjson, url, loop):
    try:
        file = getrepo(url, request)
        listjson.append(file)
        par = file()['parents']
        if (loop == 32):
            return listjson
        if  par:
            newurl = file()['parents'][0]['url']
            loop = loop +1
            commitloop(request, listjson, newurl, loop)
        else:
            return listjson
    except:
        return listjson            
    return listjson
    
def mylistcheck(mylist):
    for i in xrange(len(mylist)):
        varsplit = mylist[i].split('/')
        if (len(varsplit) == 5):
            if (varsplit[2] != "api.github.com" ):
                mylist[i] = "https://api.github.com/repos/" + varsplit[3] + "/" + varsplit[4].replace('.git','')
    return mylist



        #settings.BASE_DIR + "/repos/zip_download/"
        #with zipfile.ZipFile(r'C:\ap\repos\\' + file_name, "r") as z: z.extractall(r'C:\ap\repos\\')
        #shutil.rmtree('path', onerror=set_rw)
        #test  = file()['parents'][0]['sha']
        #newurl = 'https://api.github.com/repos/' + user  + '/' + repo + '/commits/' + file()['parents'][0]['sha']

"""    
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
"""
