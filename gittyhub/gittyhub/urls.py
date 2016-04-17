"""gittyhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'mainapp.views.index'),
    url(r'^mainapp/', include('mainapp.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^thanks/', 'mainapp.views.thanks'),
    url(r'^download/(?P<owner>[-\w]+)/(?P<repo>\w+)/(?P<fork>\w+)/$', 'mainapp.views.download'),
    #url(r'^partner/(?P<author>[-\w]+)/(?P<video>\w+)/(?P<related>\w+)/$', 'video_player'),
]
