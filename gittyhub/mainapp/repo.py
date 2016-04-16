from django import forms
import urllib.request, json

def getrepo(valu):
    with urllib.request.urlopen(valu) as url: s = url.read()
    return s
    