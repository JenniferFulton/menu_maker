from django.db import models
import re
import bcrypt
import datetime

class UserManager(models.Manager):
    def register_validator(self, postData):
    #Validate user entry upon registration 
        errors = {}
        check_user = User.objects.filter(email = postData['email'])

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be atleast 2 characters'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be atleast 2 characters'

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'
        
        if len(check_user) != 0:
            errors['duplicate_email'] = 'Email already registered, please use a different email to resister'
        
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be atleast 8 characters'

        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = 'Passwords do not match'
        
        if len(postData['city']) <= 2:
            errors['city'] = 'Please enter a valid city'
        
        if len(postData['state']) != 2:
            errors['state'] = "Please enter your state's initals. Ex: MD for Maryland"
        
        return errors
    
    def login_validator(self, postData):
    #Validates a user trying to log in 
        errors = {}
        check_user = User.objects.filter(email = postData['logemail'])

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['logemail']):
            errors['email'] = 'Please provide valid email address'
        
        if len(check_user) == 0:
            errors['no_user'] = 'User does not exist, please register first'

        elif not bcrypt.checkpw(postData['logpassword'].encode(), check_user[0].password.encode()):
            errors['invalid_pw'] = 'Password does not match username'

        return errors
    
    def update_validator(self, postData):
    #Validates user entry when they update their profile 
        errors = {}
        check_user = User.objects.filter(email = postData['new_email'])

        if len(postData['new_first_name']) < 2:
            errors['first_name'] = 'First name should be atleast 2 characters'

        if len(postData['new_last_name']) < 2:
            errors['last_name'] = 'Last name should be atleast 2 characters'

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['new_email']):
            errors['email'] = 'Invalid email address'
        
        if len(check_user) != 0:
            errors['duplicate_email'] = 'Email already registered, please use a different email to resister'
        
        if len(postData['new_city']) <= 2:
            errors['city'] = 'Please enter a valid city'
        
        if len(postData['new_state']) != 2:
            errors['state'] = "Please enter your state's initals. Ex: MD for Maryland"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    objects = UserManager()