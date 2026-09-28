from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import RegistrationForm,LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
def registration_view(request):
     if request.method=="POST":
          form=RegistrationForm(request.POST)
          if form.is_valid():
               username=form.cleaned_data.get("username")
               password=form.cleaned_data.get("password")
               email=form.cleaned_data.get("email")
               user=User.objects.create_user(username=username,password=password,email=email)
               return redirect('users:login')
     else:
        form=RegistrationForm()
     context={'form':form}
     return render(request,'auth_forms/register.html',context)

def login_view(request):
     if (request.method=="POST"):
          form=LoginForm(request.POST)
          username=""
          password=""
          if form.is_valid():
               username=form.cleaned_data.get("username")
               password=form.cleaned_data.get("password")
          user=authenticate(request,username=username,password=password)
          if user:
               login(request,user)
               return redirect('core:home')
          else:
                form.add_error(None, "Invalid username or password")
     else:
          form=LoginForm()
     context={'form':form}
     return render(request,'auth_forms/login.html',context)     
               
@login_required        
def logout_view(request):
     if request.method=='POST':
          logout(request)
          return redirect('users:login')
     else :
          return redirect('core:home')

