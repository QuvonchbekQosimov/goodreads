from django.urls import path

from books.views import BooksView, BooksDetailsView, AddReviewView

app_name = "books"

urlpatterns = [
    path("", BooksView.as_view(), name="list"),
    path("<int:id>/", BooksDetailsView.as_view(), name="detail"),
    path('<int:id>/reviews/', AddReviewView.as_view(), name='add_review'),
]
