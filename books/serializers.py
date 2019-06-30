import datetime

from rest_framework import serializers

from .models import Book


class ExternalBookSerializer(serializers.ModelSerializer):
    authors = serializers.ListField(
        child=serializers.CharField(max_length=200)
    )
    number_of_pages = serializers.IntegerField(source='numberOfPages')
    release_date = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ('name', 'isbn', 'authors', 'number_of_pages', 'publisher', 'country', 'release_date')
    
    def get_release_date(self, obj):
        release_date = obj['released']
        return datetime.datetime.strptime(release_date, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.ListField(
        child=serializers.CharField(max_length=200)
    )
    class Meta:
        model = Book
        fields = ('name', 'isbn', 'authors', 'number_of_pages', 'publisher', 'country', 'release_date')
