from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article


class ArticlesListView(ListView):
    template_name = "shopapp/article_list.html"
    # model = Article
    queryset = (Article.objects
                .defer("content")
                .select_related("author")
                .select_related("category")
                .prefetch_related("tags")
                .order_by('pk'))
    context_object_name = "articles"

