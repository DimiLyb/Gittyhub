from django import forms
import urllib.request, json, shutil, os, zipfile

def getrepo(valu):
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    with urllib.request.urlopen(valu) as url: s = url.read()
    r = getjson(s)
    return r
    
    # byte to json
def getjson(valu):
    valu = valu.decode("utf-8")
    data = json.loads(valu)
    return data

def getfile(url, file_name):
    filename = os.path.join('C:/ap/repos', file_name)
    with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:shutil.copyfileobj(response, out_file)
    getunzip(file_name)
    
def getunzip(file_name):
    with zipfile.ZipFile(r'C:\ap\repos\\' + file_name, "r") as z: z.extractall(r'C:\ap\repos\\')