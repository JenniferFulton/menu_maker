from django.shortcuts import render, redirect
from login.models import *

def home_page(request):
    #Checks if user is logged in
    if 'user' not in request.session:
        return redirect('/')
    
    #will be redirected to home page once logged in or registered
    active_user = User.objects.get(id = request.session['user'])
    context = {
        'user': active_user
    }
    return render(request,'home_page.html', context)
