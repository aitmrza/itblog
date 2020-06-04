from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    author = models.ForeignKey(
        to='Author', on_delete=models.CASCADE,
        related_name="articles", null=True, blank=True
    )

    def __str__(self):
        return self.title
    

class Author(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
