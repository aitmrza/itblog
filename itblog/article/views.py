from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import ArticleForm, AuthorForm, CommentForm
from .models import Article, Author, Comment, Tag, User


def homepage(request):
    if 'key_word' in request.GET:
        key = request.GET.get('key_word')
        articles = Article.objects.filter(
        Q(active=True),
        Q(title__contains=key) | Q(text__contains=key) | 
        Q(tag__name__contains=key) | Q(comments__text__contains=key) |
        Q(picture__contains=key) | Q(readers__username__contains=key)
        )
        articles = articles.distinct()
    else:
        articles = Article.objects.filter(active=True)

    return render(request, "article/homepage.html", {"articles": articles})

def article(request, id):
    article = Article.objects.get(id=id)
    article.views += 1
    user = request.user
    if not user.is_anonymous:
        article.readers.add(user)
    article.save()
    if request.method == "POST":
        if "delete_btn" in request.POST:
            article.active = False
            article.save()
            return redirect(homepage)
        elif "comment_btn" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                user = request.user
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
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            # Запрашиваемый пользователь становится автором
            if not Author.objects.filter(user=request.user):
                article = Author(
                    user=request.user,
                    name=request.name.username
                )
                author.save()
            else:
                author = Author.objects.get(user=request.user)

            article = Article()
            article.author = author
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.picture = form.cleaned_data['picture']
            article.save()

            # Настройка тегов
            tags = form.cleaned_data['tags']
            for tag in tags.split(','):
                if len(tag) > 0:
                    obj, created = Tag.objects.get_or_create(name=tag)
                    article.tag.add(obj)

            article.save()
            return render(request, "success.html")
    context = {}
    context['form'] = ArticleForm()
    context['protected'] = 'Сайт защищён от SQL-инъекций'
    return render(request, 'article/add_article.html', context)

def edit_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.picture = form.cleaned_data['picture']
            article.save()

            tags = form.cleaned_data['tags']
            for tag in tags.split(','):
                if len(tag) > 0:
                    obj, created = Tag.objects.get_or_create(name=tag)
                    article.tag.add(obj)

            article.save()
            context = {}
            context['article'] = article
            context['form'] = CommentForm()
            context['message'] = 'Статья изменена успешно'
            return render(request, 'article/article.html', context)

    context = {}
    context['form'] = ArticleForm(instance=article)
    context['protected'] = 'Сайт защищён от SQL-инъекций'
    return render(request, 'article/add_article.html', context)

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
    context = {}
    context['form'] = CommentForm(instance=comment)
    context['protected'] = 'Сайт защищён от SQL-инъекций'
    return render(request, 'article/comment_form.html', context)

def delete_comment(request, id):
    Comment.objects.get(id=id).delete()
    return render(request, 'success.html')
