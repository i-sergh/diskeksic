#from cProfile import Profile
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
            return redirect('signin')
        
        
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

def logout(request):
    auth.logout(request)
    return redirect('signin')
