from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from uuid import uuid4


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    is_verified = models.BooleanField(default=False)
    interests = ArrayField(models.CharField(max_length=128), blank=True)
    rating = models.IntegerField()
    postal_address = models.CharField(max_length=1024)
    phone_no = models.CharField(max_length=15)
    wallet = models.IntegerField(default=100)
    short_description = models.TextField(default='')
    books_requested_by = ArrayField(models.JSONField(), blank=True, default=[])

    def __str__(self):
        return f'<User {self.username}, {self.email}>'


class InterestedTopic(models.Model):
    interest_id = models.CharField(default=uuid4().hex)
    interest_names = ArrayField(models.CharField(max_length=128), blank=True)


"""
    0 - available
    1 - request
    2 - borrowed
"""

class BooksRequested(models.Model):
    book_id = models.IntegerField()
    issuer_user_id = models.IntegerField()
    borrower_user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book_state = models.IntegerField()
