from rest_framework import serializers


class ExternalBookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    isbn = serializers.CharField(max_length=50)
    authors = serializers.ListField(
        child=serializers.CharField(max_length=200)
    )
    number_of_pages = serializers.IntegerField(source='numberOfPages')
    publisher = serializers.CharField(max_length=200)
    country = serializers.CharField(max_length=200)
    release_date = serializers.DateTimeField(format=="%d-%m-%Y", source='released')
