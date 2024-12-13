from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
def handleRequest(request : HttpRequest):
    print(request.user)