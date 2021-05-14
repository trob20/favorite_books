from django.db import models
from datetime import date, datetime
import re


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be at least 2 characters"

        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address"

        try:
            user = User.objects.get(email = postData['email'])
            errors["emailNotUnique"] = "Email already exists, enter a different email"
        except User.DoesNotExist:
            email = None

        if len(postData["password"]) < 8:
            errors["password"] = "Password should be at least 8 characters"

        if postData["password"] != postData["confirm_password"]:
            errors["password"] = "Passwords do not match"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    # book_uploaded - one-to-many
    # favorites - many-to-many


class BookManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData["title"]) is None:
            errors["title"] = "Title is required"

        if len(postData["desc"]) < 5:
            errors["desc"] = "Description should be at least 5 characters"
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name = "book_uploaded", on_delete=models.CASCADE)
    favorite = models.ManyToManyField(User, related_name = "favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()