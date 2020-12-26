from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.article, name='article'),
    path('edit/<int:id>', views.edit_article, name='edit-article'),
    path('add', views.add_article, name='add-article'),
    path('all/<str:tag>', views.tag_articles, name='articles'),
]
