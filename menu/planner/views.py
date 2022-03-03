from django.shortcuts import render, redirect
from login.models import *
from .models import *
from django.contrib import messages

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

def user_recipes(request, id):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    
    #will redirect to a page to all the recipes they have added, with a form to add another recipe
    user_info = User.objects.get(id = id)
    context = {
        'user' : user_info,
    }
    return render(request,'user_recipes.html',context)

def all_recipes(request):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    
    #will redirect to a page to all the recipes added by all users, with a form to add another recipe
    active_user = User.objects.get(id = request.session['user'])
    all_recipes = Recipe.objects.all()
    user_recipes = active_user.recipes.all()
    context = {
        'user' : active_user,
        'all_recipes': all_recipes,
        'user_recipes' : user_recipes
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
    
def add_recipe(request, id):
    if request.method == "POST":
        #Checks if user is logged in
        if 'user' not in request.session:
            return redirect('/')

        # will run recipe through validator before creation 
        errors = Recipe.objects.newRecipe_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/planner/user_recipes/'+ str(id))

        else:
            # if there are no errors, a new recipe will be created
            # will create an array of the ingredients by seperating the commas
            all_ingredients = []
            ingredient = ''
            for i in (request.POST['ingredients']+ ','):
                if i != ',':
                    ingredient = ingredient + i
                else:
                    all_ingredients.append(ingredient)
                    ingredient = ''
            # will create an array of the directions by seperating the commas
            all_directions = []
            direction = ''
            for i in (request.POST['directions']+ ','):
                if i != ',':
                    direction = direction + i
                else:
                    all_directions.append(direction)
                    direction = ''
            # create a new recipe
            active_user = User.objects.get(id = request.session['user'])
            Recipe.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                prep = request.POST['prep'],
                cook = request.POST['cook'],
                ingredients = all_ingredients,
                directions = all_directions,
            )
            recipe_added = Recipe.objects.last()
            active_user.recipes.add(recipe_added)
            return redirect('/planner/user_recipes/'+ str(id))

def delete_recipe(request, id):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')

    #will delete a user's quote (can only delete their own)
    to_delete = Recipe.objects.get(id=id)
    to_delete.delete()
    return redirect('/planner/all_recipes')

def recipe_info(request, id):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    
    active_user = User.objects.get(id = request.session['user'])
    current_recipe = Recipe.objects.get(id=id)
    user_recipes = active_user.recipes.all()
    context = {
        'user' : active_user,
        'recipe' : current_recipe,
        'user_recipes': user_recipes,
    }
    return render(request, 'recipe_info.html', context)

def edit_recipe(request, id):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')

    active_user = User.objects.get(id = request.session['user'])
    current_recipe = Recipe.objects.get(id=id)
    context = {
        'user' : active_user,
        'recipe' : current_recipe,
    }
    return render(request, 'edit_recipe.html', context)

def update_recipe(request, id):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')

# will run recipe through validator before creation 
    errors = Recipe.objects.updateRecipe_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/planner/edit_recipe/' + str(id))

    else:
        # if there are no errors, recipe will be updated
        # will create an array of the ingredients by seperating the commas
        all_ingredients = []
        ingredient = ''
        for i in (request.POST['new_ingredients']+ ','):
            if i != ',':
                ingredient = ingredient + i
            else:
                all_ingredients.append(ingredient)
                ingredient = ''
        # will create an array of the directions by seperating the commas
        all_directions = []
        direction = ''
        for i in (request.POST['new_directions']+ ','):
            if i != ',':
                direction = direction + i
            else:
                all_directions.append(direction)
                direction = ''
        # create a new recipe
        to_edit = Recipe.objects.get(id=id)
        
        to_edit.title = request.POST['new_title']
        to_edit.description = request.POST['new_description']
        to_edit.prep = request.POST['new_prep']
        to_edit.cook = request.POST['new_cook']
        to_edit.ingredients = all_ingredients
        to_edit.directions = all_directions
        to_edit.save()
        messages.success(request, 'Recipe successfully updated!')

        return redirect('/planner/edit_recipe/' + str(id))