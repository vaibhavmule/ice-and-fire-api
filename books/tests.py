import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import Book
from .serializers import BookSerializer

client = Client()


class ExternalBookTest(TestCase):
    """Test External Book api."""

    def test_external_book(self):
        response = client.get('/api/external-books')
        data = response.data['data']
        self.assertEqual(response.data['status_code'], 200)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(len(data))


class ExternalBookByNameTest(TestCase):
    """Test External Book by name api."""

    def test_external_book_by_name(self):
        response = client.get('/api/external-books?name=A Game of Thrones')
        expected_data = {
            "status_code": 200,
            "status": "success",
            "data": [
                {
                    "name": "A Game of Thrones",
                    "isbn": "978-0553103540",
                    "authors": [
                        "George R. R. Martin"
                    ],
                    "number_of_pages": 694,
                    "publisher": "Bantam Books",
                    "country": "United States",
                    "release_date": "1996-08-01"
                }
            ]
        }
        self.assertEqual(response.data, expected_data)


class GetAllBooksTest(TestCase):
    """Test GET all books API."""

    def setUp(self):
        book_1 = {
            "id": 1,
            "name": "A Game of Thrones",
            "isbn": "978-0553103540",
            "authors": [
                "George R. R. Martin"
            ],
            "number_of_pages": 694,
            "publisher": "Bantam Books",
            "country": "United States",
            "release_date": "1996-08-01"
        }
        book_2 = {
            "id": 2,
            "name": "A Clash of Kings",
            "isbn": "978-0553108033",
            "authors": [
                "George R. R. Martin"
            ],
            "number_of_pages": 768,
            "publisher": "Bantam Books",
            "country": "United States",
            "release_date": "1999-02-02"
        }
        Book.objects.create(**book_1)
        Book.objects.create(**book_2)

    def test_get_all_books(self):
        response = client.get('/api/v1/books/')
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data, {
            "status_code": 200,
            "status": "success",
            "data": serializer.data
        })
        self.assertEqual(response.status_code, 200)


class RetriveBookTest(TestCase):
    """Test GET single book API."""

    def setUp(self):
        book_1 = {
            "id": 1,
            "name": "A Game of Thrones",
            "isbn": "978-0553103540",
            "authors": [
                "George R. R. Martin"
            ],
            "number_of_pages": 694,
            "publisher": "Bantam Books",
            "country": "United States",
            "release_date": "1996-08-01"
        }
        book_2 = {
            "id": 2,
            "name": "A Clash of Kings",
            "isbn": "978-0553108033",
            "authors": [
                "George R. R. Martin"
            ],
            "number_of_pages": 768,
            "publisher": "Bantam Books",
            "country": "United States",
            "release_date": "1999-02-02"
        }
        self.book_1 = Book.objects.create(**book_1)
        self.book_2 = Book.objects.create(**book_2)

    def test_retrive_book(self):
        response = client.get('/api/v1/books/1/')
        book = Book.objects.get(pk=self.book_1.pk)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, {
            "status_code": 200,
            "status": "success",
            "data": serializer.data
        })
        self.assertEqual(response.status_code, 200)

    def test_retrive_invalid_book(self):
        response = client.get('/api/v1/books/100000/')
        self.assertEqual(response.status_code, 404)


class CreateBookTest(TestCase):
    """Test Create Books"""

    def setUp(self):
        self.payload = {
            "name": "My First Book",
            "isbn": "123-3213243567",
            "authors": [
                "John Doe"
            ],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-08-01"
        }

    def test_create_book(self):
        response = client.post(
            '/api/v1/books/',
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)


class UpdateBookTest(TestCase):
    """Test update existing book"""

    def setUp(self):
        book_1 = {
            "id": 1,
            "name": "My First Updated Book",
            "isbn": "123-3213243567",
            "authors": [
                "John Doe"
            ],
            "number_of_pages": 350,
            "publisher": "Acme Books Publishing",
            "country": "United States",
            "release_date": "2019-01-01"
        }
        self.book_1 = Book.objects.create(**book_1)
        self.payload = {
            "name": "My First Updated Book",
            "isbn": "123-3213243567",
            "authors": [
                "John Doe"
            ],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-08-01"
        }

    def test_update_book(self):
        response = client.put(
            f'/api/v1/books/{self.book_1.pk}/',
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'The book My First Updated Book was updated successfully')


class DeleteBookTest(TestCase):
    """Test to delete exiting book"""

    def setUp(self):
        book_1 = {
            "id": 1,
            "name": "A Game of Thrones",
            "isbn": "978-0553103540",
            "authors": [
                "George R. R. Martin"
            ],
            "number_of_pages": 694,
            "publisher": "Bantam Books",
            "country": "United States",
            "release_date": "1996-08-01"
        }
        self.book_1 = Book.objects.create(**book_1)

    def test_delete_book(self):
        response = client.delete(f'/api/v1/books/{self.book_1.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_delete_book(self):
        response = client.delete(f'/api/v1/books/100000/')
        self.assertEqual(response.status_code, 404)
