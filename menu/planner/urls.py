from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('user_recipes/<int:id>', views.user_recipes),
    path('all_recipes', views.all_recipes),
    path('favorite_recipes', views.favorite_recipes),
    path('add_recipe/<int:id>', views.add_recipe),
    path('remove_favorite/<int:id>', views.remove_favorite),
    path('delete_recipe/<int:id>', views.delete_recipe),
    path('recipe_info/<int:id>', views.recipe_info),
    path('edit_recipe/<int:id>', views.edit_recipe),
    path('update/<int:id>', views.update_recipe),
    path('add_favorite/<int:id>', views.add_favorite),
    path('create_menu', views.create_menu),
    path('delete_menu', views.delete_menu),
    path('add_menu/<int:id>', views.add_menu),
    path('delete_menu/<int:id>', views.delete_menu),
    path('view_menu', views.view_menu),
    path('grocery_list/<str:city>/<str:state>', views.groceries),
    path('add_grocery/<str:city>/<str:state>', views.add_grocery),
    path('remove_grocery/<str:city>/<str:state>/<str:item>', views.remove_grocery),
    path('grocery/view_menu/<str:city>/<str:state>', views.grocery_menu),
    path('previous_menu', views.previous_menu),
]