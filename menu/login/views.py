from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def registration_login(request):
    #root route has a form for logging in
    return render(request, 'reg_login.html')

def registration(request):
    #/registration has a form for a user to register
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
                city = request.POST['city'],
                state = request.POST['state'],
                email = request.POST['email'],
                password = hashed_pw,
            )
            new_user = User.objects.last()
            request.session['user'] = new_user.id
            return redirect('/success')
        

def login(request):
    #'/login' will verify email and password to allow user to login
    #if there are errors user will be redirected to login page
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
    #'/success' takes user to the home page after logging in
    if 'user' not in request.session:
        return redirect('/')
    else:
        return redirect('planner/')

def my_account(request,id):
    #'/account/id' shows user information and allows user to update information
    if 'user' not in request.session:
        return redirect('/')

    logged_user = User.objects.get(id=id)
    context = {
        'user' : logged_user
    }
    return render(request, 'edit_account.html', context)

def edit_account(request,id):
    #'/edit/id' updates user information
    #if there are errors user will be redirected to editing page
    if 'user' not in request.session:
        return redirect('/')
    
    if request.method == "POST":
        errors = User.objects.update_validator(request.POST)
        to_edit = User.objects.get(id=id)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/account/'+str(id))

        else:
            to_edit.first_name = request.POST['new_first_name']
            to_edit.last_name = request.POST['new_last_name']
            to_edit.email = request.POST['new_email']
            to_edit.city = request.POST['new_city']
            to_edit.state = request.POST['new_state']
            to_edit.save()
            messages.success(request, 'Successfully updated your profile!')
        return redirect('/account/'+str(id))

def logout(request):
    #'/logout' logs out current user
    request.session.clear()
    return redirect('/')
