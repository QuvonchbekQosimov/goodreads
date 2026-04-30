from django.contrib import admin

from books.models import Book, Author, BookAuthor, BookReview


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'isbn')
    list_display = ('title', 'description', 'isbn')


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email',)


class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ('book', 'author')


class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ('CustomUser', 'book', 'comment', 'stars_given')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
