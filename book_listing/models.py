from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class ListedBooks(models.Model):
    added_by_user_ids = models.ArrayField(models.IntegerField(null=False))
    book_name = models.CharField(max_length=512)
    author_name = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<User {self.user}, {self.username}, {self.email}>'
