from django.shortcuts import render
from django.contrib.auth.models import User
from basic_app.forms import Userform,UserProfileform

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def index(request):
    return render(request,'basic_app/index.html')

#@login_required
def UserIndex(request):
    UserDict = {'u_name':request.user.username}
    return render(request,'basic_app/user_index.html',context=UserDict)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = Userform(data=request.POST)
        profile_form = UserProfileform(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registerd = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = Userform()
        profile_form = UserProfileform()

    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                                'profile_form':profile_form,
                                'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('user_index')

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Login failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request,'basic_app/login.html',{})
