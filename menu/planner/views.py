from django.shortcuts import render, redirect
from login.models import *

def home_page(request):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    
    #will be redirected to home page once logged in or registered
    active_user = User.objects.get(id = request.session['user'])
    context = {
        'user': active_user
    }
    return render(request,'home_page.html', context)

def groceries(request):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    
    # will redirect to page with grocery list on it
    active_user = User.objects.get(id = request.session['user'])
    context = {
        'user' : active_user
        # all ingredients for the week will be here
    }
    return render(request,'grocery_list.html', context)

def user_recipes(request):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    
    #will redirect to a page to all the recipes they have added, with a form to add another recipe
    active_user = User.objects.get(id = request.session['user'])
    context = {
        'user' : active_user
    }
    return render(request,'user_recipes.html',context)

def all_recipes(request):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    
    #will redirect to a page to all the recipes added by all users, with a form to add another recipe
    active_user = User.objects.get(id = request.session['user'])
    context = {
        'user' : active_user
    }
    return render(request,'all_recipes.html',context)

def favorite_recipes(request):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    
    #will redirect to a page to all the recipes they have favorited, with a form to add another recipe
    active_user = User.objects.get(id = request.session['user'])
    context = {
        'user' : active_user
    }
    return render(request,'favorite_recipes.html',context)

def add_recipe(request):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    
    return redirect('planner/user_recipes')