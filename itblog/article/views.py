from django.shortcuts import render
from .models import Article, Author, User


def homepage(request):
    articles = Article.objects.all()

    return render(request, "article/homepage.html",
        {"articles": articles})


def authors(request):
    authors = Author.objects.all()
    return render(request, "article/authors.html", {"authors": authors})

def users(request):
    users = User.objects.all()
    return render(request, "article/users.html", {'users': users})