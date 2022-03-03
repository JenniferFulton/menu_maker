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
        
        # if postData['prep']
        # if postData['cook']

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
        errors = {}

        if len(postData['new_title']) <= 3:
            errors['new_title'] = 'Recipe title must be atleast 3 characters'
        
        if len(postData['new_description']) <= 10:
            errors['new_description'] = "Recipe's description must have more than 10 characters"
        
        # if postData['new_prep']
        # if postData['new_cook']

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = RecipeManager()

# class Menu(models.Model):
#     week_date = models.DateField()
#     mon = models.ForeignKey()
#     tues = models.ForeignKey()
#     wed = models.ForeignKey()
#     thrus = models.ForeignKey()
#     fri = models.ForeignKey()
#     sat = models.ForeignKey()
#     sun = models.ForeignKey()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
    # objects = MenuManager()
