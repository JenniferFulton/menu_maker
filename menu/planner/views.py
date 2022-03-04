from django.shortcuts import render, redirect
from login.models import *
from .models import *
from django.contrib import messages

def home_page(request):
    #planner/ route will redirect user to home page once logged in or registered
    #Checks if user is logged in first 
    if 'user' not in request.session:
        return redirect('/')
    
    active_user = User.objects.get(id = request.session['user'])
    context = {
        'user': active_user
    }
    return render(request,'home_page.html', context)

def groceries(request):
    # planner/grocery_list will redirect to page with grocery list on it
    #Checks if user is logged in first
    if 'user' not in request.session:
        return redirect('/')
    
    active_user = User.objects.get(id = request.session['user'])
    context = {
        'user' : active_user
        # all ingredients for the week will be here
    }
    return render(request,'grocery_list.html', context)

def user_recipes(request, id):
    #planner/user_recipes/id will redirect to a page, with a form to add another recipe, and display recipes user has added 
    #Checks if user is logged in first
    if 'user' not in request.session:
        return redirect('/')
    
    user_info = User.objects.get(id = id)
    context = {
        'user' : user_info,
    }
    return render(request,'user_recipes.html',context)

def all_recipes(request):
    #planner/all_recipes will redirect to a page to all the recipes added by all users, with a form to add another recipe
    #Checks if user is logged in first
    if 'user' not in request.session:
        return redirect('/')
    
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
    #planner/favorite_recipes will redirect to a page to all the recipes a user has favorited, with a form to add another recipe
    #Checks if user is logged in first
    if 'user' not in request.session:
        return redirect('/')
    
    active_user = User.objects.get(id = request.session['user'])
    context = {
        'user' : active_user
    }
    return render(request,'favorite_recipes.html',context)
    
def add_recipe(request, id):
    #planner/add_recipe/id will add recipe after validations and redirect user to their recipes 
    #Checks if user is logged in first 
    if 'user' not in request.session:
        return redirect('/')

    if request.method == "POST":
        errors = Recipe.objects.newRecipe_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/planner/user_recipes/'+ str(id))

        else:
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

            Recipe.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                prep = request.POST['prep'],
                cook = request.POST['cook'],
                ingredients = all_ingredients,
                directions = all_directions,
            )
            active_user = User.objects.get(id = request.session['user'])
            recipe_added = Recipe.objects.last()
            active_user.recipes.add(recipe_added)
            return redirect('/planner/user_recipes/'+ str(id))

def delete_recipe(request, id):
    #planner/delete_recipe/id will delete a user's recipe (can only delete their own)
    #Checks if user is logged in frist
    if 'user' not in request.session:
        return redirect('/')

    to_delete = Recipe.objects.get(id=id)
    to_delete.delete()
    return redirect('/planner/all_recipes')

def recipe_info(request, id):
    #planner/recipe_info will diaply all info about a recipe
    #Checks if user is logged in first
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
    #planner/edit_recipe will render a page that has a form to edit a recipe (can only edit a recipe if they are the creator)
    #Checks if user is logged in first
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
    #planner/update_recipe/id will update a recipe that is trying to be edited after running it thorugh validations
    #Checks if user is logged in first
    if 'user' not in request.session:
        return redirect('/')
    
    if request.method == "POST":
        errors = Recipe.objects.updateRecipe_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/planner/edit_recipe/' + str(id))

        else:
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

def create_menu(request):
    #planner/create_menu will render a page that has a form to make a new menu for the week
    #Checks if user is logged in first
    if 'user' not in request.session:
        return redirect('/')
    
    active_user = User.objects.get(id = request.session['user'])
    all_recipes = Recipe.objects.all()
    context = {
        'user': active_user,
        'all_recipes': all_recipes
    }
    return render(request, 'create_menu.html', context)

def add_menu(request, id):
    #planne/add_menu Will add a menu
    #Checks if user is logged in first
    if 'user' not in request.session:
        return redirect('/')
    
    if request.method == "POST":
        Menu.objects.create(
            week_date = request.POST['week_date'],
            mon = request.POST['mon'],
            tues = request.POST['tues'],
            wed = request.POST['wed'],
            thrus = request.POST['thurs'],
            fri = request.POST['fri'],
            sat = request.POST['sat'],
            sun = request.POST['sun'],
        )

        return redirect('/planner')