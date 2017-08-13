#-*-coding:utf-8-*-
from django.shortcuts import render
from django.views.generic import View
from base_assistant.forms import VersionFileForm, VerinfoFileFormModel, SearchForm
from base_assistant.models import VersionInfo, Solution, MMLCmdInfo, ResponsibilityField
from django.template import Context
from django.template.loader import render_to_string
from django.http import HttpResponse
import json
import os

def parser_verinfo_file(filename):
    print(filename)
    para = dict()
    file = open(filename)
    alllines = file.readlines()
    print(alllines)
    for eachline in alllines:
        info = eachline.split(':')
        if info.size() != 2:
            print(info.size())
            return False
        else:
            para[info[0]] = info[1]

    print(para)
    return True;

def infos2verinform(infos, verinfo_model):
    print("info2ver")
    if len(infos) < 4:
        return
    print(infos)
    for i in range(0,3):
        if infos[i][0] == '产品型号' or infos[i][0] == '\ufeffproduct_type':
            verinfo_model.product = infos[i][1]
        elif infos[i][0] == '平台版本' or infos[i][0] == 'platform_ver':
            verinfo_model.platform_ver = infos[i][1]
        elif infos[i][0] == '产品版本' or infos[i][0] == 'product_ver':
            verinfo_model.product_ver = infos[i][1]
        else:
            return

    info = ""
    for i in range(3,len(infos)):
        info += infos[i][0];
        info += ","
        info += infos[i][1];
        info += ";"
    print(info)
    verinfo_model.verinfo = info
    return

def handle_verinfo_file(file):
    base_dir = os.path.dirname(os.path.abspath(__name__))
    textdir = os.path.join(base_dir, 'static', 'upload');
    filename = os.path.join(textdir, file.name);
    verinfo_model = VersionInfo()
    infos = []

    #for test
    if not os.path.exists(filename):
        return verinfo_model
    else:
        fileobj = open(filename, 'wb+')
        for chrunk in file.chunks():
            fileobj.write(chrunk)
        fileobj.close()

    #解析文件
    with open(filename, 'rb+') as f:
        lines = [x.decode('utf8').strip() for x in f.readlines()]
        for line in lines:
            infos.append(line.split(':',1))

    print(infos)
    infos2verinform(infos, verinfo_model)
    return verinfo_model

# Create your views here.
class TestAddContent(View):
    def get(self, request):
        print(request)
        para = dict()
        uf = VersionFileForm()
        para['uf'] = uf;
        return render(request, "admin_add_content.html", para)

    def post(self, request):
        paras = dict()
        if self.request.method == "POST":
            #表单获取
            version_file = VersionFileForm(self.request.POST, self.request.FILES)
            verinfo_form = VerinfoFileFormModel(self.request.POST)
            #提交了文件表单
            if version_file.is_valid():
                file = self.request.FILES.get('verinfo_file')
                if file != None:
                    verinfo = handle_verinfo_file(file)
                    verinfo_formmodel = VerinfoFileFormModel(instance=verinfo)
                    paras['verinfo_form'] = verinfo_formmodel
                    paras['uf'] = version_file
                    return render(request, "admin_add_content.html", paras)
            #提交了版本信息
            elif verinfo_form.is_valid():
                verinfo_form.save();
                paras['uf'] = VersionFileForm()
                return render(request, "admin_add_content.html", paras)
        #提交空表单
        else:
            paras['uf'] = VersionFileForm()
        return render(request, "admin_add_content.html", paras)


class TestAssistant(View):
    def get(self, request):
        print("assis")
        return render(request, "assistant_page.html")
    def post(self, request):
        return render(request, "assistant_page.html")



class TestHomePage(View):
    def get(self, request):
        form = SearchForm()
        paras = dict()
        paras['search'] = form
        return render(request, "assistant_page.html", paras)
    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            cmdinfo = MMLCmdInfo.objects.filter(cmdname__icontains=query)
            #context = Context({"query":query, "cmdinfos":cmdinfo})
            context = dict({"query": query, "cmdinfos": cmdinfo})
            return_str = render_to_string('partials/_cmdmml_search.html', context)
            print(return_str)
            return HttpResponse(json.dumps(return_str),content_type="application/json")
        return render(request, "assistant_page.html.html")