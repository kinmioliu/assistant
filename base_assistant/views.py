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

    if not os.path.exists(filename):
        print("exist file")
        return "exist file"
    else:
        fileobj = open(filename, 'wb+')
        for chrunk in file.chunks():
            fileobj.write(chrunk)
        fileobj.close()
    fileobjs = open(filename)
    alllines = fileobjs.readlines()
    print(alllines)

#        parser_verinfo_file(filename)
    return "yes"


# Create your views here.
class TestHomePage(View):
    def get(self, request):
        print(request)
        print("get")
        return render(request, "admin_add_content.html")
    def post(self, request):
        if self.request.method == "POST":
            print(self.request.FILES)
            version_file = VersionFileForm(self.request.POST, self.request.FILES)
            print(version_file.is_valid())
            if version_file.is_valid():
                print("valid")
                print(version_file)

            file = self.request.FILES.get('verinfo_file')
            handle_verinfo_file(file)

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