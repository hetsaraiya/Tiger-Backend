from django.shortcuts import render, HttpResponse

def home(request):
    return HttpResponse("<img src='/static/logo.png' style='display: block; margin: auto; width: 50%; height: auto;' alt='logo'>")