from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from books.forms import ReviewForm
from books.models import Book, BookReview


class BooksView(ListView):
    model = Book

    template_name = 'books/list.html'
    context_object_name = 'books'
    queryset = Book.objects.all().order_by('-id')
    paginate_by = 8

    def get_queryset(self):
        queryset = Book.objects.all().order_by('-id')
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        return queryset


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


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        form = ReviewForm(request.POST)

        if form.is_valid():
            BookReview.objects.create(
                book=book,
                CustomUser=request.user,
                stars_given=form.cleaned_data['stars_given'],
                comment=form.cleaned_data['comment']
            )

        return redirect(reverse('books:detail', kwargs={'id': book.id}))
