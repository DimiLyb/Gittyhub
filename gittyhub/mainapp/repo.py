from django import forms
import urllib.request, json

def getrepo(valu):
    with urllib.request.urlopen(valu) as url: s = url.read()
    r = getjson(s)
    return r
    
    # byte to json
def getjson(valu):
    valu = valu.decode("utf-8")
    data = json.loads(valu)
    return data