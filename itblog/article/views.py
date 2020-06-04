from django.shortcuts import render
from .models import Article, Author


def homepage(request):
    articles = Article.objects.all()
    wind = Author.objects.get(id=1)

    return render(request, "article/homepage.html", 
        {   
            "articles": articles,
            "wind": wind
        })