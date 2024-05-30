from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy
from .models import Author, Article, Tag, Category, ArticleR

# Create your views here.

class ArticleListView(ListView):
    template_name = 'blogapp/article-list.html'
    queryset = Article.objects.select_related("category").prefetch_related('author').prefetch_related('tag')
    context_object_name = 'articles'

class ArticlesListView(ListView):
    queryset = (
        ArticleR.objects
        .filter(published_at__isnull=False)
        .order_by("-published_at")
    )

class ArticleDetailView(DetailView):
    model = ArticleR


class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes addition blog articles"
    link = reverse_lazy("blogapp:articles")

    def items(self):
        return (
           ArticleR.objects
           .filter(published_at__isnull=False)
           .order_by("-published_at")[:5]
        )

    def item_title(self, item: ArticleR):
        return item.title

    def item_description(self, item: ArticleR):
        return item.body[:200]

    # def item_link(self, item: ArticleR):
    #     return reverse("blogapp:article", kwargs={"pk":item.pk})