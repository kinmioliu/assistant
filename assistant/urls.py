"""assistant URL Configuration

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
from base_assistant.views import TestHomePage, TestAssistant,TestTDSPage, RTN300, TestTDS, ContributeSolution, MakePolicy, download_policy_excample, MakeMMLInfo, download_mml_excample, TDS, SearchResultPage, SolutionTree

urlpatterns = [
    url(r'^rtn300/$', RTN300.as_view()),
    url(r'^contribute/$', ContributeSolution.as_view()),
    url(r'make-policy/$', MakePolicy.as_view()),
    url(r'download_policy/$', download_policy_excample),
    url(r'make-verinfo/$', MakePolicy.as_view()),
    url(r'download_verinfo/$', download_policy_excample),
    url(r'make-mml/$', MakeMMLInfo.as_view()),
    url(r'download_mml/$', download_mml_excample),
    url(r'^rtn300/tds/$', TestTDS.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^$', TestHomePage.as_view()),
#    url(r'^search/$', TestTDSPage.as_view()),
    url(r'^search/$', TestTDSPage.as_view()),
    url(r'^searchresult/', TDS.as_view()),
    url(r'^result/', SearchResultPage.as_view()),
    url(r'^solution_tree/', SolutionTree.as_view()),
]
