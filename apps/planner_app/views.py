# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Trip, Joined
import bcrypt

def index(request):
    print 'index method'
    return render(request, 'planner_app/index.html')

def submit(request):
    errors = User.objects.basic_validator(request.POST)
    if request.POST['formtype'] == 'register':
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        else:
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'], password=password)
    elif request.POST['formtype'] == 'login':
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        else:
            user_info = User.objects.get(email_address=request.POST['email_address'])
            request.session['first_name'] = user_info.first_name 
            request.session['id'] = user_info.id
            password = bcrypt.checkpw(request.POST['password'].encode(), user_info.password.encode())
            if request.POST['email_address'] == user_info.email_address and password == True:
                return redirect('travels/dashboard')
    return redirect('/')

def add(request):
    return render(request, 'planner_app/add.html')

def create(request):
    new_destination = request.POST['destination']
    current_user = User.objects.get(first_name=request.session['first_name'])
    current_user_id = current_user.id
    Trip.objects.create(destination=new_destination, travel_from=request.POST['travel_from'], travel_to=request.POST['travel_to'], user=current_user, desc=request.POST['desc'])
    return redirect('travels/dashboard')

def dashboard(request):
    current_user = User.objects.get(first_name=request.session['first_name'])
    current_user_id = current_user.id
    trips = Trip.objects.filter(user_id=current_user_id)
    joined_trips = Joined.objects.all()
    other_trips = Trip.objects.all()
    return render(request, 'planner_app/logged_in.html', {'your_trips': trips, 'other_trips': other_trips, 'all_joined': joined_trips})

def view(request, trip_id):
    current_trip = Trip.objects.get(id=trip_id)
    place = current_trip.destination
    planner_id = current_trip.user_id
    planner = User.objects.get(id=planner_id)
    joined = Joined.objects.filter(trip_id=trip_id)
    print joined
    return render(request, 'planner_app/view.html', {'place': place, 'planner': planner.first_name, 'desc': current_trip.desc, 'start': current_trip.travel_from, 'end': current_trip.travel_to, 'all_joined': joined})

def join(request, trip_id):
    current_user = User.objects.get(first_name=request.session['first_name'])
    current_user_id = current_user.id
    Joined.objects.create(user=User.objects.get(id=current_user_id), trip=Trip.objects.get(id=trip_id))
    return redirect('my_dash')

def logout(request):
    print request.session['first_name']
    request.session.flush()
    return redirect('/')