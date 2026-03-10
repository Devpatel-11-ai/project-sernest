from django.shortcuts import render,redirect,HttpResponse
from .forms import UserSignupForm,UserLoginForm
from django.contrib.auth import authenticate,login
from .models import Category, ServiceProvider
from django.http import JsonResponse

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

    categories = Category.objects.all()

    if request.method == "POST":

        name = request.POST.get("provider_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        category_id = request.POST.get("category")
        city = request.POST.get("service_area")
        experience = request.POST.get("experience")
        work_type = request.POST.get("work_type")
        mode = request.POST.get("mode")

        category = Category.objects.get(id=category_id)

        ServiceProvider.objects.create(
            name=name,
            phone=phone,
            email=email,
            category=category,
            city=city,
            experience=experience,
            work_type=work_type,
            mode=mode
        )

    return render(request, "provider_register.html", {
        "categories": categories
    })

def categories(request):

    home_services = Category.objects.filter(group="home")
    professional_services = Category.objects.filter(group="professional")
    skilled_services = Category.objects.filter(group="skilled")

    return render(request, "categories.html", {
        "home_services": home_services,
        "professional_services": professional_services,
        "skilled_services": skilled_services
    })
    
def category_providers(request, id):

    category = Category.objects.get(id=id)

    providers = ServiceProvider.objects.filter(category=category)

    return render(request, "category_providers.html", {
        "category": category,
        "providers": providers
    })

def search_categories(request):
    query = request.GET.get('', '')

    results = []

    if query:
        categories = Category.objects.filter(name__icontains=query)[:8]

        for cat in categories:
            results.append({
                "id": cat.id,
                "name": cat.name
            })

    return JsonResponse(results, safe=False)