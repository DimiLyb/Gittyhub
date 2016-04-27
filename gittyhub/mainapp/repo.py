#from django.shortcuts import render
#from django.http import HttpResponse, HttpResponseRedirect
#from django import forms
#from http import cookies
#from http.client import HTTPSConnection
#from base64 import b64encode

import urllib.request, json, zipfile, git, sys, os.path, requests, shutil, platform
#os, base64, urllib.response, urllib.parse, stat, 

from gittyhub import settings 


def getrepo(valu , request):
    #with urllib.request.urlopen(valu, auth=requests.auth.HTTPBasicAuth('', '')) as url: s = url.read()
    #r = getjson(s)
    login = request.session.get('login')
    passw = request.session.get('passw')
    r = requests.get(valu, auth=(login, passw))
    return r.json
    
    # byte to json
def getjson(valu):
    valu = valu.decode("utf-8")
    data = json.loads(valu)
    return data

def getfile(url, file_name):
    plat = platform.system()
    filename = ""
    filename = os.path.join(settings.BASE_DIR + '/repos/zip_download/', file_name)       
    with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:shutil.copyfileobj(response, out_file)
    getunzip(file_name)
    
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
    
def set_rw(operation, name, exc):
    os.chmod(name, stat.S_IWRITE)
    return True

    #shutil.rmtree('path', onerror=set_rw)