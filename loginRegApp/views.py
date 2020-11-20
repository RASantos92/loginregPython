from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from django.http import HttpResponseRedirect
from . models import *



def index(request):
    if "userId" not in request.session:
        request.session['userId'] = None
    return render(request, "index.html")

def addUser(request):
    print(request.POST)
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        securedPass= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        oneUser = User.objects.create(userName=request.POST['userName'],firstName=request.POST['firstName'],lastName=request.POST['lastName'],email=request.POST['email'],password=securedPass)
        request.session['userId'] = oneUser.id
        return redirect('/userPage')

    return redirect('/userPage')

def userPage(request):
    if "userId" not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['userId'])
        }
    return render(request, "loginPage.html", context)

def loginUser(request):
    #send the request.POST to the validator
    valErrors = User.objects.loginValidator(request.POST)
    if len(valErrors) > 0:
        for value in valErrors.values():
            messages.error(request, value)
        return redirect('/')
    else:
        usersWithEmail = User.objects.filter(email = request.POST['email'])
        request.session['userId'] = usersWithEmail[0].id
        return redirect('/userPage')

def destroySession(request):
    request.session.clear()
    return redirect('/')