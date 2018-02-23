# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

emailregex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
nameregex = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if postData['formtype'] == 'register':
            if len(postData['email_address']) < 1:
                errors['email_address'] = 'Email field cannot be empty.'
            elif not emailregex.match(postData['email_address']):
                errors['email_address'] = 'Invalid email address.'
            elif len(postData['first_name']) < 1:
                errors['first_name'] = 'First name field cannot be empty.'
            elif not nameregex.match(postData['first_name']):
                errors['first_name'] = 'First Name must be alphabetical characters only.'
            elif len(postData['last_name']) < 1:
                errors['last_name'] = "Last name field cannot be empty."
            elif not nameregex.match(postData['last_name']):
                errors['last_name'] = 'Last Name must be alphabetical characters only.'
            elif len(postData['password']) < 9:
                errors['password'] = 'Password must be more than 8 characters.'
            elif len(postData['passwordcheck']) < 9:
                errors['password'] = 'Password must be more than 8 characters.'
            elif postData['password'] != postData['passwordcheck']:
                errors['password'] = 'Password does not match password confirmation.'
            return errors
        elif postData['formtype'] == 'login':
            try:
                user_info = User.objects.get(email_address=postData['email_address'])
                password = bcrypt.checkpw(postData['password'].encode(), user_info.password.encode())
                if len(postData['password']) == 0 and password == False:
                    errors['password'] = 'Password field cannot be empty.'
                elif postData['email_address'] != user_info.email_address or password != True:
                    errors['password'] = 'Your email and password do not match. Please try again.'
                return errors
            except User.DoesNotExist:
                if len(postData['email_address']) == 0:
                    errors['email_address'] = 'Email field cannot be empty.'
                elif len(postData['password']) == 0:
                    errors['password'] = 'Password field cannot be empty.'
                elif not emailregex.match(postData['email_address']):
                    errors['email_address'] = 'Invalid email address.'
                else:
                    errors['email_address'] = 'Not a registered user. Please register or try again.'
                return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    total_trips = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    travel_from = models.CharField(max_length=255)
    travel_to = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="users")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Joined(models.Model):
    user = models.ForeignKey(User, related_name="travelers")
    trip = models.ForeignKey(Trip, related_name="trips")