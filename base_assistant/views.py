from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class TestHomePage(View):
    def get(self, request):
        print(request)
        print("get")
        return render(request, "jquery_test.html")
    def post(self, request):
        return render(request, "homepage.html")