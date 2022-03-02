from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('grocery_list', views.groceries),
    path('user_recipes/<int:id>', views.user_recipes),
    path('all_recipes', views.all_recipes),
    path('favorite_recipes', views.favorite_recipes),
    path('add_recipe', views.add_recipe),
    path('delete_recipe/<int:id>', views.delete_recipe),
]