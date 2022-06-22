from django.shortcuts import render, redirect
from login.models import *
from .models import *
from django.contrib import messages
import requests

# Authentication is checked on every route in the planner app

def home_page(request):
    #'planner/' takes user to the home page
    if 'user' not in request.session:
        return redirect('/')
    
    active_user = User.objects.get(id = request.session['user'])
    menu = Menu.objects.all()
    context = {
        'user': active_user,
        'current_menu' : menu,
    }
    return render(request,'home_page.html', context)

def view_menu(request):
    # '/view_menu' allows user to see menu on the home page they selected from a drop down selection
    if 'user' not in request.session:
        return redirect('/')

    if request.method == "POST":
        active_user = User.objects.get(id = request.session['user'])
        menu = Menu.objects.get(id = request.POST['view_menu'])
        context = {
            'user': active_user,
            'current_menu' : menu,
        }
        return render(request,'home_page.html', context)

def user_recipes(request, id):
    #'user_recipes/id' displays recipes added by user who is logged in. Can also add new recipe from this page
    if 'user' not in request.session:
        return redirect('/')
    
    user_info = User.objects.get(id = id)
    context = {
        'user' : user_info,
    }
    return render(request,'user_recipes.html',context)

def all_recipes(request):
    #'all_recipes' displays recipes added by all users, with a form to add another recipe. Can also add new recipe from this page
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
    #'favorite_recipes' displays all the recipes a user has favorited/liked. Can also add new recipe from this page
    if 'user' not in request.session:
        return redirect('/')
    
    active_user = User.objects.get(id = request.session['user'])
    context = {
        'user' : active_user
    }
    return render(request,'favorite_recipes.html',context)
    
def add_recipe(request, id):
    #'add_recipe/id' will add recipe after validations and redirect to user's recipe page 
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
    #'delete_recipe/id' will delete a user's recipe (can only delete their own)
    if 'user' not in request.session:
        return redirect('/')

    to_delete = Recipe.objects.get(id=id)
    print(type(to_delete))
    to_delete.delete()
    return redirect('/planner/all_recipes')

def recipe_info(request, id):
    #'recipe_info' displays information about selected recipe
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
    #'edit_recipe/id' displays a form to edit a recipe (can only edit a recipe if they are the creator)
    if 'user' not in request.session:
        return redirect('/')

    active_user = User.objects.get(id = request.session['user'])
    current_recipe = Recipe.objects.get(id=id)
    ingredients = current_recipe.ingredients
    context = {
        'user' : active_user,
        'recipe' : current_recipe,
        'ingredients': ingredients,
    }
    return render(request, 'edit_recipe.html', context)

def update_recipe(request, id):
    #'update_recipe/id' updates a recipe after validations
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

def add_favorite(request,id):
    # 'add_favorite/id' adds a recipe to user's favorited recipes
    if 'user' not in request.session:
        return redirect('/')

    active_user = User.objects.get(id = request.session['user'])
    liked_recipe = Recipe.objects.get(id=id)
    active_user.liked.add(liked_recipe)
    return redirect('/planner/all_recipes')

def create_menu(request):
    #'create_menu' displays a form to make a new menu for the week
    if 'user' not in request.session:
        return redirect('/')
    
    active_user = User.objects.get(id = request.session['user'])
    all_recipes = Recipe.objects.all()
    menu = Menu.objects.all()
    context = {
        'user': active_user,
        'all_recipes': all_recipes,
        'current_menu': menu
    }
    return render(request, 'create_menu.html', context)

grocery_list = []
def add_menu(request, id):
    #'add_menu' creates a new menu
    if 'user' not in request.session:
        return redirect('/')
    
    if request.method == "POST":
        errors = Menu.objects.menu_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/planner/create_menu')
        Menu.objects.create(
            week_date = request.POST['week_date'],
            mon = Recipe.objects.get(id=request.POST['mon']),
            tues = Recipe.objects.get(id=request.POST['tues']),
            wed = Recipe.objects.get(id=request.POST['wed']),
            thrus = Recipe.objects.get(id=request.POST['thurs']),
            fri = Recipe.objects.get(id=request.POST['fri']),
            sat = Recipe.objects.get(id=request.POST['sat']),
            sun = Recipe.objects.get(id=request.POST['sun']),
            )

        active_user = User.objects.get(id = request.session['user'])
        menu_added = Menu.objects.last()
        active_user.menus.add(menu_added)

        grocery_list.clear()
        grocery_list.append(menu_added.mon.ingredients)
        grocery_list.append(menu_added.tues.ingredients)
        grocery_list.append(menu_added.wed.ingredients)
        grocery_list.append(menu_added.thrus.ingredients)
        grocery_list.append(menu_added.fri.ingredients)
        grocery_list.append(menu_added.sat.ingredients)
        grocery_list.append(menu_added.sun.ingredients)
        return redirect('/planner')

def previous_menu(request):
    #'previous_menu' displays a menu that the user has selected to view
    if 'user' not in request.session:
        return redirect('/')

    if request.method == "POST":
        active_user = User.objects.get(id = request.session['user'])
        all_recipes = Recipe.objects.all()
        menu = Menu.objects.get(id = request.POST['view_menu'])
        context = {
            'user': active_user,
            'all_recipes': all_recipes,
            'current_menu' : menu,
        }
        return render(request,'create_menu.html', context)

def delete_menu(request, id):
    #'delete_menu/id' will delete a user's menu (can only delete their own)
    if 'user' not in request.session:
        return redirect('/')
    
    to_delete = Menu.objects.get(id=id)
    to_delete.delete()

    return redirect('/planner')

# arrays created for the grocery list
# produce = []
# snacks = []
# bakery = []
# intl = []
# meat = []
# bread = []
# bake_spice = []
# frozen = []
# dairy = []
# other = []

def groceries(request,city,state):
# 'grocery_list' displays a working grocery list
    if 'user' not in request.session:
        return redirect('/')

    active_user = User.objects.get(id = request.session['user'])
    foods = Food.objects.all()
    menu = Menu.objects.all()
    response = requests.get(f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=grocery%20in%20{city},{state}&key=')
    data = response.json()
    context = {
        'all_foods': foods,
        'user' : active_user,
        # 'produce': produce,
        # 'snacks': snacks,
        # 'bakery': bakery,
        # 'intl': intl,
        # 'meat': meat,
        # 'bread': bread,
        # 'bake_spice': bake_spice,
        # 'frozen': frozen,
        # 'dairy': dairy,
        # 'other': other,
        'current_menu': menu,
        'groceries': grocery_list,
        'results': data['results']
    }
    return render(request,'grocery_list.html', context)

def create_food(request,city,state):
    #'create_food' creates a food that can be used in the grocery list
    if 'user' not in request.session:
        return redirect('/')
    
    # if request.method == "POST":
    #     errors = Food.objects.food_validator(request.POST)
    #     if len(errors) > 0:
    #         for key, value in errors.items():
    #             messages.error(request, value)
    #         return redirect('/planner/grocery_list')

    #     Food.objects.create(
    #         name = request.POST['name'],
    #         category = request.POST['category']
    #     )
        return redirect(f'/planner/grocery_list/{city}/{state}')

def add_grocery(request,city,state):
    # 'add_grocery' adds food into the array associated with the category
    if 'user' not in request.session:
        return redirect('/')

    # if request.method == "POST":
        # to_add = Food.objects.get(id=request.POST['add_grocery'])
        # if to_add.category == "Produce":
        #     produce.append(to_add)

        # if to_add.category == "Snacks":
        #     snacks.append(to_add)
        
        # if to_add.category == "Bakery":
        #     bakery.append(to_add)
        
        # if to_add.category == "International":
        #     intl.append(to_add)

        # if to_add.category == "Meat":
        #     meat.append(to_add)
        
        # if to_add.category == "Bread":
        #     bread.append(to_add)
        
        # if to_add.category == "Baking & Spices":
        #     bake_spice.append(to_add)
        
        # if to_add.category == "Frozen":
        #     frozen.append(to_add)
        
        # if to_add.category == "Dairy":
        #     dairy.append(to_add)
        
        # if to_add.category == "Other":
        #     other.append(to_add)
        
        return redirect(f'/planner/grocery_list/{city}/{state}')

def remove_grocery(request,id,city,state):
    # 'remove_grocery/id' removes food into the array associated with the category
    if 'user' not in request.session:
        return redirect('/')
    
    # to_remove = Food.objects.get(id=id)
    # if to_remove.category == "Produce":
    #     produce.remove(to_remove)

    # if to_remove.category == "Snacks":
    #     snacks.remove(to_remove)
    
    # if to_remove.category == "Bakery":
    #     bakery.remove(to_remove)
    
    # if to_remove.category == "International":
    #     intl.remove(to_remove)

    # if to_remove.category == "Meat":
    #     meat.remove(to_remove)
    
    # if to_remove.category == "Bread":
    #     bread.remove(to_remove)
    
    # if to_remove.category == "Baking & Spices":
    #     bake_spice.remove(to_remove)
    
    # if to_remove.category == "Frozen":
    #     frozen.remove(to_remove)
    
    # if to_remove.category == "Dairy":
    #     dairy.remove(to_remove)
    
    # if to_remove.category == "Other":
    #     other.remove(to_remove)
    return redirect(f'/planner/grocery_list/{city}/{state}')

def grocery_menu(request,city,state):
    #'grocery/view_menu' will display the menu selected by the user on the grocery list
    if 'user' not in request.session:
        return redirect('/')

    if request.method == "POST":
        foods = Food.objects.all()
        active_user = User.objects.get(id = request.session['user'])
        menu = Menu.objects.get(id = request.POST['view_menu'])
        response = requests.get(f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=grocery%20in%20{city},{state}&key=')
        data = response.json()
        context = {
            'user': active_user,
            'current_menu' : menu,
            'all_foods': foods,
            'user' : active_user,
            # 'produce': produce,
            # 'snacks': snacks,
            # 'bakery': bakery,
            # 'intl': intl,
            # 'meat': meat,
            # 'bread': bread,
            # 'bake_spice': bake_spice,
            # 'frozen': frozen,
            # 'dairy': dairy,
            # 'other': other,
            'groceries': grocery_list,
            'results': data['results']
        }
        return render(request,'grocery_list.html', context)
    



