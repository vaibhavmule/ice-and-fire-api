from django.test import TestCase, Client
from django.urls import reverse

client = Client()

class ExternalBookTest(TestCase):
    """Test External Book api."""

    def test_external_book(self):
        response = client.get('/api/external-books')
        data = response.data['data']
        self.assertEqual(response.data['status_code'], 200)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(len(data))

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
