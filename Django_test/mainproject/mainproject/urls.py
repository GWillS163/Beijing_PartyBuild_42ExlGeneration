"""mainproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from scorerank import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'', views.index),
    path(r'', views.alllist),
    # path(r'^calpage/', views.calPag),
    url(r'^calpage/', views.calPag),
    url(r'^receive_query_score$', views.receive_query_score),
    url(r'^receive_query_rank$', views.receive_query_rank),
    url(r'^receive$', views.receive),
    url(r'^alllist', views.alllist),
    url(r'^del', views.DelData),

    # API
    url(r'^getalllist', views.api_alllist),
    url(r'^api_getRank/from=<int:down_strict>-to=<int:up_strict>-by=<str:client>/', views.api_getRank, name="api_getRank"),

]
