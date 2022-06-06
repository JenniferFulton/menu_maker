from django.shortcuts import render, redirect
from login.models import *
from .models import *
from django.contrib import messages
import requests

def home_page(request):
    #planner/ route will redirect user to home page once logged in or registered
    #Checks if user is logged in first 
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
    #Checks if user is logged in first 
    if 'user' not in request.session:
        return redirect('/')

    if request.method == "POST":
        active_user = User.objects.get(id = request.session['user'])
        menu = Menu.objects.get(id = request.POST['view_menu'])
        context = {
            'user': active_user,
            'current_menu' : menu,
        }
        return render(request,'selected_menu.html', context)

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

# def remove_recipe(request, id):
#     #Will remove the relationship between Recipe and User before deleting 
#     #Checks if user is logged in frist
#     if 'user' not in request.session:
#         return redirect('/')

#     to_delete = Recipe.objects.get(id=id)
#     active_user = User.objects.get(id = request.session['user'])
#     to_delete.entry.remove(active_user)
#     return redirect('/planner/delete_recipe/' + str(id))

def delete_recipe(request, id):
    #planner/delete_recipe/id will delete a user's recipe (can only delete their own)
    #Checks if user is logged in frist
    if 'user' not in request.session:
        return redirect('/')

    to_delete = Recipe.objects.get(id=id)
    print(type(to_delete))
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
    ingredients = current_recipe.ingredients
    context = {
        'user' : active_user,
        'recipe' : current_recipe,
        'ingredients': ingredients,
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

def add_favorite(request,id):
    # Will add a recipe to user's favorited recipes
    #Checks if user is logged in first
    if 'user' not in request.session:
        return redirect('/')

    active_user = User.objects.get(id = request.session['user'])
    liked_recipe = Recipe.objects.get(id=id)
    active_user.liked.add(liked_recipe)
    return redirect('/planner/all_recipes')

def create_menu(request):
    #planner/create_menu will render a page that has a form to make a new menu for the week
    #Checks if user is logged in first
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

def add_menu(request, id):
    #planner/add_menu Will add a menu
    #Checks if user is logged in first
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
        return redirect('/planner')

def previous_menu(request):
#Checks if user is logged in first 
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
    #Checks if user is logged in first 
    if 'user' not in request.session:
        return redirect('/')
    
    to_delete = Menu.objects.get(id=id)
    to_delete.delete()

    return redirect('/planner')

produce = []
snacks = []
bakery = []
intl = []
meat = []
bread = []
bake_spice = []
frozen = []
dairy = []
other = []

def groceries(request):
# planner/grocery_list will redirect to page with grocery list on it
#Checks if user is logged in first
    if 'user' not in request.session:
        return redirect('/')

    active_user = User.objects.get(id = request.session['user'])
    foods = Food.objects.all()
    menu = Menu.objects.all()
    context = {
        'all_foods': foods,
        'user' : active_user,
        'produce': produce,
        'snacks': snacks,
        'bakery': bakery,
        'intl': intl,
        'meat': meat,
        'bread': bread,
        'bake_spice': bake_spice,
        'frozen': frozen,
        'dairy': dairy,
        'other': other,
        'current_menu': menu,
    }
    return render(request,'grocery_list.html', context)

def create_food(request):
    #Checks if user is logged in first
    if 'user' not in request.session:
        return redirect('/')
    
    if request.method == "POST":
        errors = Food.objects.food_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/planner/grocery_list')

        Food.objects.create(
            name = request.POST['name'],
            category = request.POST['category']
        )
        return redirect('/planner/grocery_list')

def add_grocery(request):
    if 'user' not in request.session:
        return redirect('/')

    if request.method == "POST":
        to_add = Food.objects.get(id=request.POST['add_grocery'])
        if to_add.category == "Produce":
            produce.append(to_add)

        if to_add.category == "Snacks":
            snacks.append(to_add)
        
        if to_add.category == "Bakery":
            bakery.append(to_add)
        
        if to_add.category == "International":
            intl.append(to_add)

        if to_add.category == "Meat":
            meat.append(to_add)
        
        if to_add.category == "Bread":
            bread.append(to_add)
        
        if to_add.category == "Baking & Spices":
            bake_spice.append(to_add)
        
        if to_add.category == "Frozen":
            frozen.append(to_add)
        
        if to_add.category == "Dairy":
            dairy.append(to_add)
        
        if to_add.category == "Other":
            other.append(to_add)
        
        return redirect('/planner/grocery_list')

def remove_grocery(request,id):
    if 'user' not in request.session:
        return redirect('/')
    
    to_remove = Food.objects.get(id=id)
    if to_remove.category == "Produce":
        produce.remove(to_remove)

    if to_remove.category == "Snacks":
        snacks.remove(to_remove)
    
    if to_remove.category == "Bakery":
        bakery.remove(to_remove)
    
    if to_remove.category == "International":
        intl.remove(to_remove)

    if to_remove.category == "Meat":
        meat.remove(to_remove)
    
    if to_remove.category == "Bread":
        bread.remove(to_remove)
    
    if to_remove.category == "Baking & Spices":
        bake_spice.remove(to_remove)
    
    if to_remove.category == "Frozen":
        frozen.remove(to_remove)
    
    if to_remove.category == "Dairy":
        dairy.remove(to_remove)
    
    if to_remove.category == "Other":
        other.remove(to_remove)
    return redirect('/planner/grocery_list')

def grocery_menu(request):
    #Checks if user is logged in first 
    if 'user' not in request.session:
        return redirect('/')

    if request.method == "POST":
        foods = Food.objects.all()
        active_user = User.objects.get(id = request.session['user'])
        menu = Menu.objects.get(id = request.POST['view_menu'])
        context = {
            'user': active_user,
            'current_menu' : menu,
            'all_foods': foods,
            'user' : active_user,
            'produce': produce,
            'snacks': snacks,
            'bakery': bakery,
            'intl': intl,
            'meat': meat,
            'bread': bread,
            'bake_spice': bake_spice,
            'frozen': frozen,
            'dairy': dairy,
            'other': other,
        }
        return render(request,'grocery_list.html', context)
    



