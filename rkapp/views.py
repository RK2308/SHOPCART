from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
from rkapp.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"rkapp/index.html",{"Products":products})



def add_to_cart(request):
    pass

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'logout successgilly')
    return redirect('/')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,'login successsfully')
                return redirect('/')
            else:
                messages.error(request,"Invalid details")
                return redirect('/login')
        return render(request,"rkapp/login.html")



def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success you can login account...")
            return redirect('/login')
    return render(request,"rkapp/register.html",{'form':form})


def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"rkapp/collections.html",{"Catagory":catagory})
    
        
        
   

def collectionsview(request,name):
  if(Catagory.objects.filter(name=name,status=0)):
      products=Product.objects.filter(Catagory__name=name)
      return render(request,"rkapp/products/index.html",{"Products":products,"Catagory_name":name})
  
  else:
      messages.warning(request,"No such catagory found")
      return redirect('collections')
  


def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"rkapp/products/product_details.html",{"Product":products})

        else:
            messages.error(request,"No such proudect Found")
            return redirect("collections")
        

    else:
        messages.error(request,"No such proudect Found")
        return redirect("collections")
