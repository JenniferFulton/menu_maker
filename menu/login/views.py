from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def registration_login(request):
    #root route will have a form for logging in
    return render(request, 'reg_login.html')

def registration(request):
    #/registration will have a form for registration 
    return render(request, 'register.html')

def register(request):
    #'/register' will create a new user, login the user, and redirect to home page
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/registration')
        
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = hashed_pw,
            )
            new_user = User.objects.last()
            request.session['user'] = new_user.id
            return redirect('/success')
        

def login(request):
    #'/login' will verify email and password to allow user to login
    #if no errors return redirect('/success')
    #if errors return redirect('/')
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')

        else:
            logged_user = User.objects.get(email=request.POST['logemail'])
            request.session['user'] = logged_user.id
            return redirect('/success')

def success(request):
    #'/success' will redirect to examone app where the home page of the user will be with quotes
    if 'user' not in request.session:
        return redirect('/')
    else:
        return redirect('planner/')

def logout(request):
    request.session.clear()
    return redirect('/')
