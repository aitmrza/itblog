from django.shortcuts import render, redirect
from .models import Article, Author, User, Comment
from .forms import ArticleForm, AuthorForm, CommentForm

def homepage(request):
    articles = Article.objects.filter(active=True)

    return render(request, "article/homepage.html",
        {"articles": articles})

def article(request, id):
    article = Article.objects.get(id=id)
    if request.method == "POST":
        if "delete_btn" in request.POST:
            article.active = False
            article.save()
            return redirect(homepage)

        elif "comment_btn" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                user = request.user
                form.save()
                comment = Comment(
                    user=user,
                    article=article,
                    text=form.cleaned_data['text']
                )    
                comment.save()
    context = {}
    context["article"] = article
    context["form"] = CommentForm()
    return render(request, "article/article.html", context)

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "success.html")

    form = ArticleForm()
    return render(request, 'article/add_article.html', {'form': form})

def edit_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
            
    form = ArticleForm(instance=article)
    return render(request, 'article/add_article.html', {'form': form})

def authors(request):
    authors = Author.objects.all()
    return render(request, "article/authors.html", {"authors": authors})

def author(request, id):
    author = Author.objects.get(id=id)
    return render(request, 'article/author.html', {"author": author})

def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "success.html")
    
    form = AuthorForm()
    return render(request, 'article/add_author.html', {'form': form})

def users(request):
    users = {}
    users['users'] = User.objects.all()
    return render(request, "article/users.html", users)
        

def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
    form = CommentForm(instance=comment)
    return render(request, 'article/comment_form.html', {'form': form})

def delete_comment(request, id):
    Comment.objects.get(id=id).delete()
    return render(request, 'success.html')
