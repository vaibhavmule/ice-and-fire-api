import requests
from rest_framework.views import APIView
from rest_framework.response import Response

from books.serializers import ExternalBookSerializer


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
