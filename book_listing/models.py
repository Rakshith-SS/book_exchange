from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class ListedBooks(models.Model):
    added_by_user_ids = ArrayField(models.IntegerField(null=False), blank=True)
    book_name = models.CharField(max_length=512)
    author_name = models.CharField(max_length=512)
    is_deleted = models.BooleanField(default=False)
    state_manager = models.IntegerField(default=-100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    rating = models.IntegerField()
    topics = ArrayField(models.CharField(max_length=256), blank=True)
    added_by_users = ArrayField(models.CharField(max_length=512), blank=True)

    def __str__(self):
        return f'<Book {self.book_name}, {self.added_by_user_ids}, {self.author_name}, >'
