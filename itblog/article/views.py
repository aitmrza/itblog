from django.shortcuts import render, redirect
from .models import Article, Author, User
from .forms import ArticleForm, AuthorForm

def homepage(request):
    articles = Article.objects.filter(active=True)

    return render(request, "article/homepage.html",
        {"articles": articles})

def article(request, id):
    if request.method == "POST":
        article = Article.objects.get(id=id)
        article.active = False
        article.save()
        return redirect(homepage)


    article = Article.objects.get(id=id)
    return render(request, 'article/article.html',
    {"article": article})

def add_article(request):
    if request.method == 'POST':
        article = Article()
        article.title = request.POST.get('title')
        article.text = request.POST.get("text")
        author_id = request.POST.get("author")
        author = Author.objects.get(id=author_id)
        article.author = author
        article.save()
        return render(request, "success.html")

    form = ArticleForm()
    return render(request, 'article/add_article.html', {'form': form})


def authors(request):
    authors = Author.objects.all()
    return render(request, "article/authors.html", {"authors": authors})

def author(request, id):
    author = Author.objects.get(id=id)
    return render(request, 'article/author.html', {"author": author})

def add_author(request):
    if request.method == 'POST':
        author = Author()
        author.name = request.POST.get('name')
        author.save()
        return render(request, 'success.html')
    
    form = AuthorForm()
    return render(request, 'article/add_author.html', {'form': form})

def users(request):
    users = {}
    users['users'] = User.objects.all()
    return render(request, "article/users.html", users)