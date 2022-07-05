#from cProfile import Profile
import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import Profile





# Create your views here.
@login_required(login_url='signin')
def index(reqest):
    #return HttpResponse('<H1>Дискексик</H1>')
    return render(reqest, 'index.html')


    
@login_required(login_url='signin')
def user_settings(request):
    user_profile = Profile.objects.get(user=request.user)
    user = User.objects.get(username=request.user)
    
    if request.method =='POST':

        if request.FILES.get('profile_img') == None:
            image = user_profile.profileimg
        else:
            image = request.FILES.get('profile_img')
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        bio = request.POST['bio']
        location = request.POST['location']
        
        user.first_name = first_name
        user.last_name = last_name
        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        user.save()
        return redirect('user_settings')
    return render(request, 'user_settings.html', {'user_profile': user_profile}) 

def signup(request):
    
    if request.method == 'POST':

        username =  request.POST['username']
        email =  request.POST['email']  
        password =  request.POST['password'] 
        confirm_password =  request.POST['confirm_password'] 

        if password != confirm_password:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('signup')

        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('signup')

        else:
            user = User.objects.create_user(username=username,email=email, password=password)
            user.save()
               
            user_model = User.objects.get(username=username)
                
            profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            profile.save()

            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)
            return redirect('user_settings')
        
        
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user )
            return redirect('/')
        else:
            messages.info(request, ' invalid credentials ')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
