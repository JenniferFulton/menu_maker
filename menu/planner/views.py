from django.shortcuts import render, redirect
from login.models import *
from .models import *

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
    all_recipes = Recipe.objects.all()
    context = {
        'user' : active_user,
        'all_recipes': all_recipes
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
    if request.method == "POST":
        #Checks if user is logged in
        if 'user' not in request.session:
            return redirect('/')

        # will need to go through a validator first
        
        # will create an array of the ingredients by seperating the commas
        all_ingredients = []
        ingredient = ''
        for i in (request.POST['ingredients']+ ','):
            if i != ',':
                ingredient = ingredient + i
            else:
                all_ingredients.append(ingredient)
                ingredient = ''

        all_directions = []
        direction = ''
        for i in (request.POST['directions']+ ','):
            if i != ',':
                direction = direction + i
            else:
                all_directions.append(direction)
                direction = ''

        # create a new recipe
            Recipe.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                prep = request.POST['prep'],
                cook = request.POST['cook'],
                ingredients = all_ingredients,
                directions = all_directions,

            )
        return redirect('/planner/user_recipes')

def delete_recipe(request, id):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')

    #will delete a user's quote (can only delete their own)
    to_delete = Recipe.objects.get(id=id)
    to_delete.delete()
    return redirect('/planner/all_recipes')