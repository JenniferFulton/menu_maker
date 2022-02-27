from django.urls import path
from . import views

urlpatterns = [
    path('', views.registration_login),
    path('registration', views.registration),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('account/<int:id>',views.my_account),
    path('edit/<int:id>', views.edit_account),
    path('logout', views.logout),
]