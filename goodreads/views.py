from django.shortcuts import render
from django.views import View

from books.models import BookReview


def landing_page(request):
    return render(request, 'landing.html')


class HomePageView(View):
    def get(self, request):
        reviews = BookReview.objects.all().order_by('-id')

        context = {
            'reviews': reviews
        }
        return render(request, 'home.html', context)
