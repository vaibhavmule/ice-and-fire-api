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


class CreateUpdateBookSerializer(serializers.ModelSerializer):
    authors = serializers.ListField(
        child=serializers.CharField(max_length=200)
    )

    class Meta:
        model = Book
        fields = ('name', 'isbn', 'authors', 'number_of_pages', 'publisher', 'country', 'release_date')

    def create(self, validated_data):
        validated_data['authors'] = ','.join(validated_data.get('authors'))
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.authors = ','.join(validated_data.get('authors'))
        instance.number_of_pages = validated_data.get('number_of_pages', instance.number_of_pages)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.country = validated_data.get('country', instance.country)
        instance.release_date = validated_data.get('release_date', instance.release_date)
    
        instance.save()
        return instance


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'name', 'isbn', 'authors', 'number_of_pages', 'publisher', 'country', 'release_date')

    def get_authors(self, obj):
        return obj.authors.split(',')

