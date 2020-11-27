from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from article import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('authors', views.authors, name='authors'),
    path('author/profile/<int:id>', views.author_profile, name='author-profile'),
    path('author/add', views.add_author, name='add-author'),
    path('users', views.users, name='users'),
    path('article/<int:id>', views.article, name='article'),
    path('article/edit/<int:id>', views.edit_article, name='edit-article'),
    path('article/add/', views.add_article, name='add-article'),
    path('articles/<str:tag>', views.articles, name='articles'),
    path('comment/<int:id>/edit', views.edit_comment, name='edit-comment'),
    path('comment/<int:id>/delete', views.delete_comment, name='delete-comment'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
