#-*-coding:utf-8-*-
from django.shortcuts import render
from django.views.generic import View
import os
from base_assistant.forms import VersionFileForm, VerinfoFileFormModel

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

def infos2verinform(infos, verinfform):
    print(len(infos))
    if len(infos) < 3:
        verinfform.errors['err0'] = "输入文件内容非法"
        return
    lens = len(infos)
    print(lens)
    print(infos)
    for i in range(0,2):
        print(infos[i])
        if infos[i][0] == '产品' or infos[i][0] == '\ufeffproduct':
            verinfform.product = infos[i][1]
        elif infos[i][0] == '平台版本' or infos[i][0] == 'platform_ver':
            verinfform.platform_ver = infos[i][1]
        elif infos[i][0] == '产品版本' or infos[i][0] == 'product_ver':
            verinfform.product_ver = infos[i][1]
        else:
            verinfform.errors['err1'] = "参数非法"
            return

    info = ""
    for i in range(3,lens):
        print(infos[i])
        info += infos[i][0];
        info += ","
        info += infos[i][1];
        info += ";"
    print(info)
    verinfform.verinfo = info
    return

def handle_verinfo_file(file):
    base_dir = os.path.dirname(os.path.abspath(__name__))
    textdir = os.path.join(base_dir, 'static', 'upload');
    filename = os.path.join(textdir, file.name);
    verinfo_formmodel = VerinfoFileFormModel()
    infos = []

    #for test
    if not os.path.exists(filename):
        return verinfo_formmodel
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

    infos2verinform(infos, verinfo_formmodel)
    print(verinfo_formmodel.verinfo)
    return verinfo_formmodel

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
        paras = dict()
        if self.request.method == "POST":
            #表单获取
            version_file = VersionFileForm(self.request.POST, self.request.FILES)
            verinfo_form = VerinfoFileFormModel(self.request.POST)
            #提交了文件表单
            if version_file.is_valid():
                file = self.request.FILES.get('verinfo_file')
                if file != None:
                    infos = handle_verinfo_file(file)
                    print("infossss")
                    print(infos.verinfo)
                    infos.save(commit= True)
                    paras['verinfo_form'] = infos
                    paras['uf'] = version_file
                    return render(request, "admin_add_content.html", paras)
            #提交了版本信息
            elif verinfo_form.is_valid():
                verinfo_form.save();
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

class TestAddContent(View):
    def get(self, request):
        return render(request, "admin_add_content.html")
    def post(self, request):
        return render(request, "admin_add_contetn.html")