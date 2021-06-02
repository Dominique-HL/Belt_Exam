from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

#  Manager(s)

class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, confirm_password):
        validation_result = self.validate(first_name, last_name, email, password, confirm_password)
        if validation_result['status'] == True:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            created_user = self.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
            validation_result = {'status': validation_result['status'], 'created_user': created_user}
            return validation_result
        return validation_result

    def validate(self, first_name, last_name, email, password, confirm_password):
        errors = []
        result = {}
        if first_name == '':
            msg = "First name cannot be left blank"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(first_name) < 2:
            msg = "First Name should have atleast two characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in first_name) == True:
            msg = "Name cannot have numbers"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        if last_name == '':
            msg = "Last name cannot be left blank"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(last_name) < 2:
            msg = "First Name should have atleast two characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in last_name) == True:
            msg = "Name cannot have numbers"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        if email == '':
            msg = "Email cannot be left blank"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif not emailRegex.match(email):
            msg = "Email is invalid"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(self.filter(email = email)) > 0:
            msg = "Email already exist in our database"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        if password == '':
            msg = "Password cannot be left blank"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(password) < 8:
            msg = "Password must be greater than 8 characters"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif not passwordRegex.match(password):
            msg = "Password must contain at least one lowercase letter, one uppercase letter, and one digit"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif confirm_password != password:
            msg = "Passwords do not match"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        else:
            result = {'status': True, 'errors': "Validation successful"}
            return result

    def login_validate(self, email, password):
        errors = []
        try:
            found_user = self.get(email = email)
            if bcrypt.checkpw(password.encode(), found_user.password.encode()):
                result = {'status' : True, 'found_user' : found_user}
                return result
            else:
                msg = "Email and Password do not match"
                errors.append(msg)
                result = {'status' : False, 'errors' : errors[0]}
                return result
        except:
            msg = "Email is not in our database"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result

class ThoughtManager(models.Manager):
    def validate_thought(self, thought_text, user_id, thoughted_by):
        errors = []
        if len(thoughted_by) < 4:
            msg = "'thoughted by' should be not be less than 4 characters."
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(thought_text) < 10:
            msg = "thought is too short to be a thought!"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        current_user = User.objects.get(id = user_id)
        self.create(thought_text = thought_text, author = current_user, thoughted_by = thoughted_by)
        msg = "thought created."
        errors.append(msg)
        result = {'status' : True, 'errors' : errors[0]}
        return result

    def add_favourite_for_user(self, user_id, thought_id):       
        thought = Thought.objects.get(id = thought_id)
        current_user = User.objects.get(id = user_id)
        thought.favouriting_users.add(current_user)
        result = {'status': True}
        return result
    
    def remove_from_favorites(self, user_id, thought_id):
        thought = Thought.objects.get(id = thought_id)
        current_user = User.objects.get(id = user_id)
        thought.favouriting_users.remove(current_user)

        
# Create your models here.

class User(models.Model):
    first_name = models.CharField (max_length=255, null = True)
    last_name = models.CharField (max_length=45, null = True)
    email = models.CharField (max_length = 45, null = True)
    password = models.CharField (max_length=100, null = True)
    
    
    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

class Thought(models.Model):
    thought_text = models.TextField (max_length = 1000, null = True)
    author = models.ForeignKey(User, related_name="thoughts_posted", on_delete=models.CASCADE)
    created_at = models.DateTimeField (auto_now_add = True)
    favouriting_users = models.ManyToManyField(User, related_name="favourite_thoughts")
    thoughted_by = models.CharField (max_length=255, null = True)
    objects = ThoughtManager()