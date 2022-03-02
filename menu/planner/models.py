from django.db import models
from login.models import User

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
    # objects = RecipeManager()

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
