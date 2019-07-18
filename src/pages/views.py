from django.http import HttpResponse
from django.shortcuts import render

def home_view(*args, **kwargs):
    return HttpResponse("<p>こんにちは！<br>This is the Receipt server!</p>")