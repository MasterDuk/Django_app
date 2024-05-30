from django.urls import path, include
from . import views

app_name = "blogapp"


urlpatterns = [
       path('article/', views.ArticleListView.as_view(), name="article-list"),
       path('articles/', views.ArticlesListView.as_view(), name="articles"),
       path('articles/<int:pk>', views.ArticleDetailView.as_view(), name="article"),
       path('articles/latest/feed/', views.LatestArticlesFeed(), name="articles-feed"),

]

