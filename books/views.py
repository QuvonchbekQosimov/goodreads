from django.views.generic import DetailView, ListView

from books.models import Book


class BooksView(ListView):
    model = Book
    template_name = 'books/list.html'
    context_object_name = 'books'
    queryset = Book.objects.all()


class BooksDetailsView(DetailView):
    model = Book
    template_name = 'books/details.html'
    context_object_name = 'book'
    pk_url_kwarg = "id"

# class BooksView(View):
#     def get(self, request):
#         books = Book.objects.all()
#
#         return render(request, 'books/list.html', {'books': books})


# class BooksDetailsView(View):
#     def get(self, request, id):
#         book = Book.objects.get(id=id)
#         return render(request, 'books/details.html', {'book': book})
