from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core import serializers
from django.shortcuts import render
from django.views.generic import View



class MakeResponsibiltyField(LoginRequiredMixin, View):
    """制作责任田信息"""
    login_url = '/admin/'
    redirect_field_name = '/contribute/'

    def get(self, request):
        print("get make_responsibilty_field")
        paras = dict()
        return render(request, "make_responsibilty_field.html", paras)

    def post(self, request):
        print("post make_responsibilty_field")
        paras = dict()
        return render(request, "make_responsibilty_field.html", paras)
