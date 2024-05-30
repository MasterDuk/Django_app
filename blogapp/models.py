from django.db import models
from django.urls import reverse


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100, null=False,blank=True)
    bio = models.TextField(null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=40, null=False,blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False,blank=True)


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=True)
    content = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)


class ArticleR(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("blogapp:article", kwargs={"pk": self.pk})