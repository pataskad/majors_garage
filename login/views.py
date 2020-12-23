
from django.shortcuts import render, redirect
from django.conf import settings

from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        return redirect('/home')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'home.html', context)

def baseline_products(request):
    if 'user_id' not in request.session:
        return redirect('/')
    blineproducts = Product.objects.filter(category='Baseline')
    context = {
        'blineproducts': blineproducts
    }
    return render(request, 'baseline.html', context)

def driver_products(request):
    if 'user_id' not in request.session:
        return redirect('/')
    allproducts = Product.objects.filter(category='Driver')
    context = {
        'allproducts': allproducts
    }
    return render(request, 'driver.html', context)

def elite_products(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'elite.html')

def coming_soon(request):
    return render(request, 'coming-soon.html')

def checkout(request):
    return render(request, 'checkout.html')

def success(request):
    return render(request, 'success.html')