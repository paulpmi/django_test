"""umm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from youtube_clone.authentification_app.router import auth_app_urlpatterns
from youtube_clone.video_app.router import video_app_urlpatterns

app_urls = []
app_urls += auth_app_urlpatterns
app_urls += video_app_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include((app_urls, 'youtube_clone_app'))),
]
