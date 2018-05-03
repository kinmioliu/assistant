from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core import serializers
from django.shortcuts import render
from django.views.generic import View
from util.conf import DUMP
from util import conf
from django.template import Context
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import QuerySet
from util.make_responsibilty_field import ResponsibiltyFieldParser
from util.handle_resoure_code import ResourceParserManager
import os
from util.handle_fileinfo import FileInfoParser
from util.handle_scrapy_info import WikiParserManager
from util.handle_mmlevt_new import MMLEVTParserManager


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
        #获取前台参数
        if self.request.method == "POST":
            func = request.POST.get('func')
            DUMP('func: ' + func)
            if func != None:
                parser = ResponsibiltyFieldParser()
                result = parser.run()
                paras = dict()
                paras['created'] =  render_to_string('partials/_json_data.html', {'text' : 'created ' + str(len(result['created'])) + ' records' } )
                paras['updated'] =  render_to_string('partials/_json_data.html', {'text' : 'updated ' + str(len(result['updated'])) + ' records'} )
                return JsonResponse(paras)

        #提交空表单
        else:
            paras = {'result': 'err'}
            return JsonResponse(paras)

        paras = dict()
        return render(request, "make_responsibilty_field.html", paras)

class MakeFileInfo(LoginRequiredMixin, View):
    """制作责任田信息"""
    login_url = '/admin/'
    redirect_field_name = '/contribute/'

    def get(self, request):
        print("get make fileinfo")
        paras = dict()
        return render(request, "make_fileinfo.html", paras)

    def post(self, request):
        print("post make fileinfo")
        # 获取前台参数
        if self.request.method == "POST":
            func = request.POST.get('func')
            DUMP('func: ' + func)
            if func != None:
                base_dir = os.path.dirname(os.path.abspath(__name__))
                textdir = os.path.join(base_dir, 'static', 'upload');
                filepath = os.path.join(textdir, conf.FILES_PATH_DOC_NAME);
                print(filepath)
                filesinfo_file = open(filepath, 'r', encoding='UTF-8')
                lines = filesinfo_file.readlines()
                parser = FileInfoParser(lines=lines)
                result = parser.run()

                filesinfo_file.close()

                paras = dict()
                paras['created'] = render_to_string('partials/_json_data.html',
                                                    {'text': 'created ' + str(len(result['created'])) + ' records'})
                paras['updated'] = render_to_string('partials/_json_data.html',
                                                    {'text': 'updated ' + str(len(result['updated'])) + ' records'})
                return JsonResponse(paras)

        # 提交空表单
        else:
            paras = {'result': 'err'}
            return JsonResponse(paras)

        paras = dict()
        return render(request, "make_responsibilty_field.html", paras)


class MakeResourceInfo(LoginRequiredMixin, View):
    login_url = '/admin/'
    redirect_field_name = '/contribute/'

    def get(self, request):
        print("get make_resourceinfo")
        paras = dict()
        return render(request, "make_resource_info.html", paras)

    def post(self, request):
        print("post make_resource_info")
        # 获取前台参数
        if self.request.method == "POST":
            func = request.POST.get('func')
            DUMP('func: ' + func)
            if func != None:
                base_dir = os.path.dirname(os.path.abspath(__name__))
                textdir = os.path.join(base_dir, 'static', conf.ResourceFilePath);
                parser = ResourceParserManager(file_path=textdir)
                result = parser.run()
                paras = dict()
                paras['created'] = render_to_string('partials/_json_data.html',
                                                    {'text': 'created ' + str(parser.created_records) + ' records'})
                paras['updated'] = render_to_string('partials/_json_data.html',                                                    
                                                    {'text': 'updated ' + str(parser.updated_records) + ' records'})
                return JsonResponse(paras)


        # 提交空表单
        else:
            paras = {'result': 'err'}
            return JsonResponse(paras)

        paras = dict()
        return render(request, "make_resource_info.html", paras)


class MakeWikiInfo(LoginRequiredMixin, View):
    login_url = '/admin/'
    redirect_field_name = '/contribute/'

    def get(self, request):
        print("get make_wikiinfo")
        paras = dict()
        return render(request, "make_wiki_info.html", paras)

    def post(self, request):
        print("post make_wiki_info")
        # 获取前台参数
        if self.request.method == "POST":
            func = request.POST.get('func')
            DUMP('func: ' + func)
            if func != None:
                base_dir = os.path.dirname(os.path.abspath(__name__))
                textdir = os.path.join(base_dir, 'static', conf.WIKI_FILE_PATH);
                parser = WikiParserManager(file_path=textdir)
                result = parser.run()
                paras = dict()
                paras['created'] = render_to_string('partials/_json_data.html',
                                                    {'text': 'created ' + str(parser.created_records) + ' records'})
                paras['updated'] = render_to_string('partials/_json_data.html',
                                                    {'text': 'updated ' + str(parser.updated_records) + ' records'})
                return JsonResponse(paras)


        # 提交空表单
        else:
            paras = {'result': 'err'}
            return JsonResponse(paras)

        paras = dict()
        return render(request, "make_wiki_info.html", paras)



class MakeMMLEVTInfo(LoginRequiredMixin, View):
    login_url = '/admin/'
    redirect_field_name = '/contribute/'

    def get(self, request):
        print("get make_mmlevtinfo")
        paras = dict()
        return render(request, "make_mmlevt_info_new.html", paras)

    def post(self, request):
        print("post make_mmlevt_info")
        # 获取前台参数
        if self.request.method == "POST":
            func = request.POST.get('func')
            DUMP('func: ' + func)
            if func != None:
                base_dir = os.path.dirname(os.path.abspath(__name__))
                textdir = os.path.join(base_dir, 'static', conf.MMLEVT_FILE_PATH);
                parser = MMLEVTParserManager(file_path=textdir)
                result = parser.run()
                paras = dict()
                paras['created'] = render_to_string('partials/_json_data.html',
                                                    {'text': 'created ' + str(parser.created_records) + ' records'})
                paras['updated'] = render_to_string('partials/_json_data.html',
                                                    {'text': 'updated ' + str(parser.updated_records) + ' records'})
                return JsonResponse(paras)


        # 提交空表单
        else:
            paras = {'result': 'err'}
            return JsonResponse(paras)

        paras = dict()
        return render(request, "make_mmlevt_info_new.html", paras)
