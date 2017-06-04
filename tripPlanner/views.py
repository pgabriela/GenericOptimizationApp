from django.shortcuts import render, redirect
from django.contrib.auth import logout


def home(request):
    if(request.user.is_authenticated):
        return render(request, 'tripPlanner/home.html', {})
    else:
        return redirect('loginPage')


def logoutPage(request):
    logout(request)
    return redirect('loginPage')


def createGroup(request):
    if(request.user.is_authenticated):
        """todo"""
    else:
        return redirect('loginPage')
