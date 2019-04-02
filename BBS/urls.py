"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from blog import views
from django.views.static import serve
from BBS import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.register),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^login_random_code/', views.random_image),
    url(r'^media/(?P<path>.*)', serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^(?P<username>\w+)/(?P<func>category|archive|tag)/(?P<num>\d+)', views.site_detail),
    url(r'^(?P<username>\w+)/articles/(?P<article_id>\d+)$', views.article_detail),
    url(r'^like_and_against/$', views.like_and_against),
    url(r'^comment/(?P<where>\w+)', views.comment),
    url(r'^(?P<username>\w+)/$', views.site),
    url(r'^$', views.index),
]
