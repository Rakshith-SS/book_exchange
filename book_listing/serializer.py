from rest_framework import serializers
from .models import ListedBooks


class AddBookSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    book_name = serializers.CharField(min_length=3, max_length=512)
    author_name = serializers.CharField(min_length=3, max_length=512)
    description = serializers.CharField(max_length=2048)
    added_by_user = serializers.CharField(max_length=512)
    rating = serializers.IntegerField()


class GetBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListedBooks
        fields = '__all__'
