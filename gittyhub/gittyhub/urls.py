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
from django.conf.urls import include, url, patterns
from django.contrib import admin
from mainapp import views as mainapp_views
#from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', mainapp_views.index),
    url(r'^mainapp/', include('mainapp.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^thanks/', mainapp_views.thanks),
    url(r'^download/(?P<owner>[\w|\W]+)/(?P<repo>[\w|\W]+)/(?P<fork>[\w|\W]+)/$', mainapp_views.download),
    url(r'^commit/(?P<owner>[\w|\W]+)/(?P<repo>[\w|\W]+)/$', mainapp_views.commit),
    url(r'^downloadgit/(?P<owner>[\w|\W]+)/(?P<repo>[\w|\W]+)/$', mainapp_views.downloadgit),
    url(r'^jsonMC/(?P<owner>[\w|\W]+)/(?P<repo>[\w|\W]+)/(?P<fork>[\w|\W]+)/$', mainapp_views.jsonMC),
    url(r'^allcommit/(?P<owner>[\w|\W]+)/(?P<repo>[\w|\W]+)/(?P<fork>[\w|\W]+)/$', mainapp_views.allcommit),
    url(r'^allcommitnext/(?P<owner>[\w|\W]+)/(?P<repo>[\w|\W]+)/(?P<sha>[\w|\W]+)/$', mainapp_views.allcommitnext),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#old urls
    #url(r'^download/(?P<owner>[-\w]+)/(?P<repo>\w+)/(?P<fork>\w+)/$', 'mainapp.views.download'),
    #url(r'^favicon\.ico$', RedirectView.as_view(url='/static/gitty.png', permanent=True))
    #url(r'^repo', mainapp_views.setrepo),
    #url(r'^login/', mainapp_views.login),
    #url(r'^partner/(?P<author>[-\w]+)/(?P<video>\w+)/(?P<related>\w+)/$', 'video_player'),
    #url(r'^my/', mainapp_views.myview),
    #url(r'^$', mainapp_views.myview),