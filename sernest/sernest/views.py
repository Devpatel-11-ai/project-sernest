from django.http import HttpResponse
from django.shortcuts import render

#specifi url
def test(request):
    return HttpResponse("Hello")
        
# def AboutUs(request):
#     return HttpResponse("About")

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def home(request):
    return render(request,'home.html')

def categories(request):
    return render(request, 'categories.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def contact(request):
    return render(request, 'contact.html')

def provider_register(request):
    return render(request, 'provider_register.html')

def register(request):
    return render(request, 'register.html')

