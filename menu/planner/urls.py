from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('user_recipes/<int:id>', views.user_recipes),
    path('all_recipes', views.all_recipes),
    path('favorite_recipes', views.favorite_recipes),
    path('add_recipe/<int:id>', views.add_recipe),
    # path('remove_recipe/<int:id>', views.remove_recipe),
    path('delete_recipe/<int:id>', views.delete_recipe),
    path('recipe_info/<int:id>', views.recipe_info),
    path('edit_recipe/<int:id>', views.edit_recipe),
    path('update/<int:id>', views.update_recipe),
    path('add_favorite/<int:id>', views.add_favorite),
    path('create_menu', views.create_menu),
    path('add_menu/<int:id>', views.add_menu),
    path('view_menu/<int:id>', views.view_menu),
    path('grocery_list', views.groceries),
    path('create_food', views.create_food),
]