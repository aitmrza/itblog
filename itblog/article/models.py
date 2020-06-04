from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    author = models.ForeignKey(
        to='Author', on_delete=models.CASCADE,
        related_name="articles", null=True, blank=True
    )
    readers = models.ManyToManyField(to=User, related_name="articles")

    def __str__(self):
        return self.title
    

class Author(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(
        to=User, on_delete=models.SET_NULL, related_name="author",
        null=True, blank=True
    )
    
    def __str__(self):
        return self.name
