#-*-coding:utf-8-*-
from django.core import serializers
from django.shortcuts import render
from django.views.generic import View
from base_assistant.forms import VersionFileForm, VerinfoFileFormModel, SearchForm
from base_assistant.models import VersionInfo, Solution, MMLCmdInfo, ResponsibilityField
from django.template import Context
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
import json
import os
import re

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
        return render(request, "homepage.html")
    def post(self, request):
        print("post")
        return render(request, "homepage.html")

class TestTDSPage(View):
    def get(self, request):
        print("testtdspage")
        form = SearchForm()
        paras = dict()
        paras['search'] = form
        return render(request, "assistant_page.html", paras)
    def post(self, request):
        print("post hhh1")
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            cmdinfo = MMLCmdInfo.objects.filter(cmdname__icontains=query)
            #context = Context({"query":query, "cmdinfos":cmdinfo})
            context = dict({"query": query, "cmdinfos": cmdinfo})
            return_str = render_to_string('partials/_cmdmml_search.html', context)
            print(return_str)
            return HttpResponse(json.dumps(return_str),content_type="application/json")
        return HttpResponse("/search")

    def getpg_by_product(self, request, product):
        verinfos = VersionInfo.objects.filter(product=product)
        print("testtdspage")
        print(verinfos)
        form = SearchForm()
        paras = dict()
        paras['search'] = form
        return render(request, "assistant_page.html", paras)

class RTN300(TestTDSPage):
    def get(self, request):
        product = 'RTN300'
        print("testtdspage")
        return TestTDSPage.getpg_by_product(self, request, product)

class SolutionNode:
    serial_num = 0
    solution_info = ''
    def __init__(self, num, info):
        self.serial_num = num
        self.solution_info = info

    def __str__(self):
        return str(self.serial_num) + self.solution_info

class SolutionModel:
    parent = SolutionNode(0,'')
    selfinfo = SolutionNode(0,'')
    parents = dict()

    def __init__(self, parent, selfinfo):
        self.parent = parent
        self.selfinfo = selfinfo

    def __str__(self):
        return str(self.parent.serial_num) + "<-" + str(self.selfinfo.serial_num)

def parse_solution_file(path):
    path = r"F:\pyhton\project\site\assistant\templates\syserr_solution.txt"
    print(path)
    solution_file = open(path)
    lines = solution_file.readlines()
    infos = dict()
    solution_path_node = dict()
    begin_construct = False;

    for line in lines:
        #读取
        if line.find('solution]') > 0:
            print("find solution")
            begin_construct = True

        #读取数字
        elif begin_construct == False:
            solution = line.split('.', 1)
            if len(solution) == 2:
                serial_num = solution[0]
                replay = solution[1]
                if serial_num.isdigit():
                    infos[int(serial_num)] = SolutionNode(num = serial_num, info = replay)

        #开始筛选节点
        elif begin_construct == True:
            print("筛选" + line)
            nodes = line.split("->")
            size = len(nodes)
            cur_pos = 0
            for node in nodes:
                cur_pos += 1
                #若是第一个节点
                if node == nodes[0]:
                    print("cur_pos:" + str(cur_pos) + "," + node)
                    serial_num = int(node)
                    #若已经存在，就跳过
#                    if solution_path_node.has_key(serial_num):
                    if serial_num in solution_path_node:
                        print("solution_path_node.has_key(serial_num):")
                        continue;
                    # 若不存在，就创建，并加入到字典中
                    else:
                        sm = SolutionModel(parent=SolutionNode(0,''), selfinfo=infos[serial_num])
                        solution_path_node[serial_num] = sm
                #是最后一个节点
                elif node == nodes[size-1]:
                    print("cur_pos:" + str(cur_pos) + "," + node)
                    #判断是否有()
                    if node.find(')') > 0:
                        #提取()中的内容
                        substr = re.findall(r'[^()]+', node)[0]
#                        print("substr:" + substr)
                        tail_nodes = substr.split(',')
                        #(10,11,12,13)
 #                       print(tail_nodes)
                        for tail_node in tail_nodes:
                            serial_num = int(tail_node)
                            print("tail_node:" + str(serial_num))
                            # 若是中间节点，则直接创建，或者是提取上一个节点到配置
                            #if solution_path_node.has_key(serial_num):
                            if serial_num in solution_path_node:
                                #若节点存在，则刷新父亲节点
                                tmp_node = solution_path_node[serial_num]
                                tmp_node.parent = infos[int(nodes[cur_pos - 2])]
                                solution_path_node[serial_num] = tmp_node
                            else:
                                #若节点不存在，则创建
  #                              print("pre node:" + nodes[cur_pos - 2])
                                sm = SolutionModel(parent=infos[int(nodes[cur_pos - 2])], selfinfo=infos[serial_num])
                                solution_path_node[serial_num] = sm

                    else:
                        #没有节点
                        serial_num = int(tail_node)
                        # 若是中间节点，则直接创建，或者是提取上一个节点到配置
#                        if solution_path_node.has_key(serial_num):
                        if serial_num in solution_path_node:
                            # 若节点存在，则刷新父亲节点
                            tmp_node = solution_path_node[serial_num]
                            tmp_node.parent = infos[int(nodes[cur_pos - 2])]
                            solution_path_node[serial_num] = tmp_node
                        else:
                            # 若节点不存在，则创建
#                            print("pre node:" + nodes[cur_pos - 2])
                            sm = SolutionModel(parent=infos[int(nodes[cur_pos - 2])], selfinfo=infos[serial_num])
                            solution_path_node[serial_num] = sm

                else:
                    print("cur_pos:" + str(cur_pos) + "," + node)
                    serial_num = int(node)
                    #若是中间节点，则直接创建，或者是提取上一个节点到配置
#                    if solution_path_node.has_key(serial_num):
                    if serial_num in solution_path_node:
                        print("语法问题")
                        return 0xffff   #若存在，说明语法有问题
                    else:
                        sm = SolutionModel(parent=infos[int(nodes[cur_pos - 2])],selfinfo= infos[serial_num])
                        solution_path_node[serial_num] = sm

    for sm in solution_path_node:
        print(solution_path_node[sm])

#    print(infos)
    solution_file.close()
#        print(solution)

class TestTDS(View):
    def get(self, request):
        paras = dict()
        return render(request, 'tds.html', paras)

    def post(self, request):
        requestype = request.POST['requesttype']
        product = request.POST['product']
        print(requestype)
        if (requestype == 'getverinfo'):
            verinfos = VersionInfo.objects.filter(product=product)
            verinfo_ajax = serializers.serialize("json",verinfos)
            paras = {'requesttype':requestype}
            i = 0;
            for verinfo in verinfos:
                context = {"verinfo":verinfo}
                verinfo_xml_str = render_to_string('partials/_verinfo_card.html', context)
                print(verinfo_xml_str)
                paras['verinfo'+ str(i)] = verinfo_xml_str
                i += 1

            print(paras)
            return JsonResponse(paras)
        elif (requestype == 'get_relative_question'):
            path = ""
            print("path111")
            parse_solution_file(path)
            return HttpResponse("")
        return HttpResponse("")
