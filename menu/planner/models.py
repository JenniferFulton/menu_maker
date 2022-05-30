from django.db import models
from login.models import User

class RecipeManager(models.Manager):
    def newRecipe_validator(self, postData):
        # validates a recipe that is being added by a user
        errors = {}

        if len(postData['title']) <= 3:
            errors['title'] = 'Recipe title must be atleast 3 characters'
        
        if len(postData['description']) <= 10:
            errors['description'] = "Recipe's description must have more than 10 characters"
        
        if postData['prep'].isnumeric() == True or postData['prep'].isalpha() == True:
            errors['prep'] = 'Please include number and units in your Prep Time, Ex: 10 minutes'
        
        if postData['cook'].isnumeric() == True or postData['cook'].isalpha() == True:
            errors['cook'] = 'Please include number and units in your Cook Time, Ex: 20 minutes'

        commas_inIngredients = []
        for i in postData['ingredients']:
            if i == ',':
                commas_inIngredients.append(i)
        if len(commas_inIngredients) == 0:
            errors['ingredients'] = 'Please add commas between each ingredient'

        commas_inDirections = []
        for i in postData['directions']:
            if i == ',':
                commas_inDirections.append(i)
        if len(commas_inDirections) == 0:
            errors['directions'] = 'Please add commas between each direction'
        
        return errors

    def updateRecipe_validator(self, postData):
        #validates a recipe that a user is updating
        errors = {}

        if len(postData['new_title']) <= 3:
            errors['new_title'] = 'Recipe title must be atleast 3 characters'
        
        if len(postData['new_description']) <= 10:
            errors['new_description'] = "Recipe's description must have more than 10 characters"
        
        if postData['new_prep'].isnumeric() == True or postData['new_prep'].isalpha() == True:
            errors['new_prep'] = 'Please include number and units in your Prep Time, Ex: 10 minutes'
        
        if postData['new_cook'].isnumeric() == True or postData['new_cook'].isalpha() == True:
            errors['new_cook'] = 'Please include number and units in your Cook Time, Ex: 20 minutes'

        commas_inIngredients = []
        for i in postData['new_ingredients']:
            if i == ',':
                commas_inIngredients.append(i)
        if len(commas_inIngredients) == 0:
            errors['new_ingredients'] = 'Please add commas between each ingredient'

        commas_inDirections = []
        for i in postData['new_directions']:
            if i == ',':
                commas_inDirections.append(i)
        if len(commas_inDirections) == 0:
            errors['new_directions'] = 'Please add commas between each direction'
        
        return errors

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    prep = models.CharField(max_length=30, null=True)
    cook = models.CharField(max_length=30, null=True)
    ingredients = models.TextField()
    directions = models.TextField()
    entry = models.ManyToManyField(User,related_name= "recipes")
    favorite = models.ManyToManyField(User,related_name="liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = RecipeManager()

class Menu(models.Model):
    week_date = models.DateField(Recipe, null=True)
    mon = models.ForeignKey(Recipe, related_name="mon_menus", null=True, on_delete=None)
    tues = models.ForeignKey(Recipe, related_name="tues_menus", null=True, on_delete=None)
    wed = models.ForeignKey(Recipe, related_name="wed_menus", null=True, on_delete=None)
    thrus = models.ForeignKey(Recipe, related_name="thurs_menus", null=True, on_delete=None)
    fri = models.ForeignKey(Recipe, related_name="fri_menus", null=True, on_delete=None)
    sat = models.ForeignKey(Recipe, related_name="sat_menus", null=True, on_delete=None)
    sun = models.ForeignKey(Recipe, related_name="sun_menus", null=True, on_delete=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # objects = MenuManager()
