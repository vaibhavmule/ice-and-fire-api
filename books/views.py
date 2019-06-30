import requests

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import ExternalBookSerializer, BookSerializer
from .models import Book


class ExternalBook(APIView):
    """Get books from Ice and Fire API."""
    def get(self, request):
        book_name = request.query_params.get('name', '')
        serializer = ExternalBookSerializer(get_books(book_name), many=True)
        return Response({
            "status_code": 200,
            "status": "success",
            "data": serializer.data
        })


def get_books(name):
    url = f'https://www.anapioficeandfire.com/api/books?name={name}'
    r = requests.get(url)
    return r.json()


class BookViewSet(viewsets.ModelViewSet):
    """Book CRUD API"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({
            "status_code": 201,
            "status": "success",
            "data": serializer.data
        }, status=201)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status_code": 200,
            "status": "success",
            "data": serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status_code": 200,
            "status": "success",
            "data": serializer.data
        })

    def update(self, request,  *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
        return Response({
            "status_code": 200,
            "status": "success",
            "data": serializer.data
        })

    def destroy(self, request):
        instance = self.get_object()
        instance.delete()
        return Response({
            "status_code": 200,
            "status": "success",
            "message": f"The book {instance.name} was deleted successfully",
            "data": []
        })
