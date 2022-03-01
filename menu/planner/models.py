from django.db import models

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    prep_time = models.DurationField()
    cook_time = models.DurationField()
    ingredients = models.TextField()
    directions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # objects = RecipeManager()

class Menu(models.Model):
    week_date = models.DateField()
    mon = models.ForeignKey()
    tues = models.ForeignKey()
    wed = models.ForeignKey()
    thrus = models.ForeignKey()
    fri = models.ForeignKey()
    sat = models.ForeignKey()
    sun = models.ForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # objects = MenuManager()
