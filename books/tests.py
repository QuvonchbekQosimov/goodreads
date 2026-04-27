from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No books found.")

    def test_book_list(self):
        Book.objects.create(title="Book 1", description="Description 1", isbn="123456789")
        Book.objects.create(title="Book 2", description="Description 2", isbn="987654321")
        Book.objects.create(title="Book 3", description="Description 3", isbn="565897957")
        response = self.client.get(reverse("books:list"))
        books = Book.objects.all()
        for book in books:
            self.assertContains(response, book.title)
