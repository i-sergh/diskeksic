from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(reqest):
    #return HttpResponse('<H1>Дискексик</H1>')
    return render(reqest, 'index.html')


def signup(request):
    return render(request, 'signup.html')