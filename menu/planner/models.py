from django.db import models

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    ingredients = models.CharField(max_length=255)
    instructions = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # objects = RecipeManager()
    
