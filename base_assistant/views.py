from django.shortcuts import render
from django.views.generic import View
import os

# Create your views here.
class TestHomePage(View):
    def get(self, request):
        print(request)
        print("get")
        return render(request, "admin_add_content.html")
    def post(self, request):
        print("POST1")
        if self.request.method == "POST":
            print("POST")
            print(request)
            file = self.request.FILES.get('personico')
            base_dir = os.path.dirname(os.path.abspath(__name__))
            textdir = os.path.join(base_dir, 'static', 'txt');
            print(file)
            filename = os.path.join(textdir, file.name);
            print(filename)

            fobj = open(filename, 'wb');
            for chrunk in file.chunks():
                fobj.write(chrunk);
            fobj.close();

        return render(request, "homepage.html")

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