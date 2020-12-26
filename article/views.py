from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import *
from .models import Article, Author, Comment, Tag, User


def homepage(request):
    if 'key_word' in request.GET:
        # Используется фильтр статей по определенным параметрам
        key = request.GET.get('key_word')
        articles = Article.objects.filter(
            Q(active=True),
            Q(title__contains=key) | Q(text__contains=key) |
            Q(tag__name__contains=key) | Q(comments__text__contains=key) |
            Q(picture__contains=key) | Q(readers__username__contains=key)
        )
        articles = articles.distinct()
    else:
        articles = Article.objects.order_by('-publications_date').filter(active=True)

    return render(request, "article/homepage.html", {'articles': articles})


def tag_articles(request, tag):
    tag = Tag.objects.get(name=tag)
    context = {'articles': Article.objects.filter(tag=tag)}
    return render(request, 'article/articles.html', context)


def article(request, id):
    article = Article.objects.get(id=id)
    user = request.user
    article.views += 1
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

    context = {"article": article, "form": CommentForm()}
    return render(request, "article/article.html", context)


@login_required(login_url='homepage')
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            if not Author.objects.filter(user=request.user):
                author = Author(
                    user=request.user,
                    name=request.user.username
                )
                author.save()
            else:
                author = Author.objects.get(user=request.user)

            article = Article(
                author=author,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                picture=form.cleaned_data['picture'])
            article.save()

            # Настройка тегов
            tags = form.cleaned_data['tags']
            for tag in tags.split(','):
                if len(tag) > 0:
                    obj, created = Tag.objects.get_or_create(name=tag)
                    article.tag.add(obj)

            article.save()
            return render(request, "success.html")

    context = {'form': ArticleForm(), 'protected': 'Сайт защищён от SQL-инъекций'}
    return render(request, 'article/add_article.html', context)


@login_required
def edit_article(request, id):
    article = Article.objects.get(id=id)
    if article.author.user != request.user:
        raise Http404
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
            context = {'article': article, 'form': CommentForm()}
            return render(request, 'article/article.html', context)

    context = {'form': ArticleForm(instance=article)}
    return render(request, 'article/add_article.html', context)


def authors(request):
    authors = Author.objects.all()
    return render(request, "article/authors.html", {"authors": authors})


def author_profile(request, id):
    author = Author.objects.get(id=id)
    return render(request, 'article/author_profile.html', {"author": author})


def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "success.html")

    form = AuthorForm()
    return render(request, 'article/add_author.html', {'form': form})


def users(request):
    return render(request, "article/users.html", {'users': User.objects.all()})


def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(homepage)

    context = {'form': CommentForm(instance=comment)}
    return render(request, 'article/comment_form.html', context)


def delete_comment(request, id):
    Comment.objects.get(id=id).delete()
    return redirect(homepage)
