from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def index(request):
    """
    계정생성
    """
    return render(request, "index.html")