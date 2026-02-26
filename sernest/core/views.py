from django.shortcuts import render,redirect,HttpResponse
from .forms import UserSignupForm,UserLoginForm
from django.contrib.auth import authenticate,login

# Create your views here.
def UserSignupView(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'core/signup.html', {'form': form})
    else:
        form = UserSignupForm()
        return render(request, 'core/signup.html', {'form': form})
        

def UserLoginView(request):
  if request.method =="POST":
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
      print(form.cleaned_data)
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = authenticate(request,email=email,password=password) #it will check in database..
      if user:
        login(request,user)
        if user.role == 'admin':
          return redirect('admin:index')
        else:
          return redirect('home')
      else:
        return render(request,'core/login.html',{'form':form})
  else:
    form = UserLoginForm()
    return render(request,'core/login.html',{'form':form})

def home(request):
    return render(request, 'home.html')

def provider_register(request):
    return render(request, 'provider_register.html')

