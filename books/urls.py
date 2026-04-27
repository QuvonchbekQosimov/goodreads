from django.urls import path

from books.views import BooksView, BooksDetailsView

app_name = "books"

urlpatterns = [
    path("", BooksView.as_view(), name="list"),
    path("<int:id>/", BooksDetailsView.as_view(), name="detail")
]
