#-*-coding:utf-8-*-
from django.shortcuts import render
from django.views.generic import View
import os
from base_assistant.forms import VersionFileForm

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

def handle_verinfo_file(file):
    base_dir = os.path.dirname(os.path.abspath(__name__))
    textdir = os.path.join(base_dir, 'static', 'upload');
    filename = os.path.join(textdir, file.name);
    infos = []

    if not os.path.exists(filename):
        return infos
    else:
        fileobj = open(filename, 'wb+')
        for chrunk in file.chunks():
            fileobj.write(chrunk)
        fileobj.close()
    print(filename)

    #解析文件
    with open(filename, 'rb') as f:
        lines = [x.decode('utf8').strip() for x in f.readlines()]
        for line in lines:
            infos.append(line.split(':',1))

    print(infos)
    return infos

# Create your views here.
class TestHomePage(View):
    def get(self, request):
        print(request)
        print("get")
        para = dict()
        uf = VersionFileForm()
        para['uf'] = uf;
        return render(request, "admin_add_content.html", para)

    def post(self, request):
        if self.request.method == "POST":
            print(self.request.FILES)
            version_file = VersionFileForm(self.request.POST, self.request.FILES)
            print(version_file.is_valid())
            if version_file.is_valid():
                file = self.request.FILES.get('verinfo_file')
                if file != None:
                    infos = handle_verinfo_file(file)
                    paras = dict()
                    paras['infos'] = infos
                    paras['uf'] = VersionFileForm()
                    return render(request, "admin_add_content.html", paras)
        return render(request, "admin_add_content.html")


class TestAssistant(View):
    def get(self, request):
        print("assis")
        return render(request, "assistant_page.html")
    def post(self, request):
        return render(request, "assistant_page.html")

class TestAddContent(View):
    def get(self, request):
        return render(request, "admin_add_content.html")
    def post(self, request):
        return render(request, "admin_add_contetn.html")