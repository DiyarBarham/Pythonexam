from django.db import models
from datetime import datetime
import re
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['firstname']) < 2 or not re.compile(r'^[a-zA-Z]+$'):
            errors["firstname"] = "first name should be at least 2 characters"
        if len(postData['alias']) < 2:
            errors["alias"] = "last name should be at least 2 characters"

        if len(postData['passwd']) < 8 :
            errors["passwd"] = "Password description should be at least 8 characters"
        if postData['passwd']!=postData['confirmpass']:
            errors["confirmpass"] = "Passwords do not match!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):  # test whether a field matches the pattern
            errors['email'] = "Invalid email address!"
        if postData['birthday'] != '':
            dop = datetime.strptime(postData['birthday'], "%Y-%m-%d")
            age = (datetime.now() - dop).days / 365
            if age < 16:
                errors["birthday"] = "You need to be 16 years old to register"
        else:
            errors["birthday"] = "You need to enter birthday"
        return errors
class User(models.Model):
    firstname = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Friends(models.Model):
    my_id = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)
    f_id = models.ForeignKey(User, related_name='thefriend', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)