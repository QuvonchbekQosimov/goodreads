from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        url = reverse('books:list')
        response = self.client.get(url)
        self.assertContains(response, "No books found in the library yet.")

    def test_book_list(self):
        Book.objects.create(title="Book 1", description="Description 1", isbn="123456789")
        Book.objects.create(title="Book 2", description="Description 2", isbn="987654321")
        Book.objects.create(title="Book 3", description="Description 3", isbn="565897957")
        response = self.client.get(reverse("books:list"))
        books = Book.objects.all()
        for book in books:
            self.assertContains(response, book.title)

        def test_book_model_str_method(self):
            self.assertEqual(str(self.book), "Test Kitob")

        def test_pagination_is_working(self):
            for i in range(4):
                Book.objects.create(title=f"Qo'shimcha kitob {i}", description="Test uchun")

            url = reverse('books:list')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTrue('is_paginated' in response.context)
            self.assertTrue(response.context['is_paginated'])
            self.assertEqual(len(response.context['books']), 4)

        def test_search_books_by_title(self):
            Book.objects.create(title="Harry Potter", description="Sehrgarlar haqida")
            url = reverse('books:list') + "?q=Harry"
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Harry Potter")
            self.assertNotContains(response, "Test Kitob")

        def test_search_no_results(self):
            url = reverse('books:list') + "?q=BundayKitobYoq123"
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['books']), 0)
            self.assertContains(response, "No books found in the library yet.")

        def test_book_detail_404_not_found(self):
            url = reverse('books:detail', kwargs={'id': 9999})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

        def test_multiple_books_display(self):
            Book.objects.create(title="Django For Beginners", description="Django bo'yicha to'liq qo'llanma")
            Book.objects.create(title="Clean Code", description="KISS prinsipi va toza kod sirlari")
            Book.objects.create(title="Cybersecurity 101", description="Kali Linux va tarmoq xavfsizligi asoslari")
            url = reverse('books:list')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Django For Beginners")
            self.assertContains(response, "Clean Code")
            self.assertContains(response, "Cybersecurity 101")
            self.assertEqual(len(response.context['books']), 4)


class BookReviewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.book = Book.objects.create(
            title="Clean Code",
            description="Dasturlash haqida kitob",
            isbn="1234567890"
        )

    def test_add_review(self):
        self.client.login(username='testuser', password='testpassword123')

        url = reverse('books:add_review', kwargs={'id': self.book.id})
        data = {
            'stars_given': 5,
            'comment': 'Ajoyib kitob!'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookReview.objects.count(), 1)

        review = BookReview.objects.first()
        self.assertEqual(review.stars_given, 5)
        self.assertEqual(review.comment, 'Ajoyib kitob!')
        self.assertEqual(review.CustomUser, self.user)
        self.assertEqual(review.book, self.book)
