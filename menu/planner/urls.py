from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('grocery_list', views.groceries),
]