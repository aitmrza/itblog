from django.shortcuts import render
from .models import Article, Author


def homepage(request):
    articles = Article.objects.all()

    return render(request, "article/homepage.html",
        {"articles": articles})


def authors(request):
    authors = Author.objects.all()
    return render(request, "article/authors.html", {"authors": authors})