from django.shortcuts import render,redirect
from .forms import UserSignupForm

# Create your views here.
def UserSignupView(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('core:login')
        else:
            return render(request, 'core/signup.html', {'form': form})
    else:
        form = UserSignupForm()
        return render(request, 'core/signup.html', {'form': form})
        
def UserLoginView(request):
    return render(request, 'core/login.html')

def home(request):
    return render(request, 'home.html')


