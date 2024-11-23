from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ContactForm
from .forms import Client

# Create your views here.
def Menu(request):
    return render(request, 'header.html')

def Footer(request):
    return render(request, 'footer.html')

def index(request):
    return render(request, 'index.html')

def Development(request):
    return render(request, 'development.html')

def Infrastructure(request):
    return render(request, 'infrastructure.html')

def Contact(request):
    form = Client()
    return render(request, 'contact.html', {"form":form})

def PrivacyNotice(request):
    return render(request, 'privacyNotice.html')

def Merchandise(request):
    return render(request, 'merchandise.html')