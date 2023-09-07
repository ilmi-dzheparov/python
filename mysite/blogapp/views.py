from django.views.generic import ListView, DetailView

from blogapp.models import Article

from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse


class ArticlesListView(ListView):
    template_name = "shopapp/article_list.html"
    # model = Article
    queryset = (Article.objects
                # .defer("content")
                .select_related("author")
                .select_related("category")
                .prefetch_related("tags")
                .filter(pub_date__isnull=False)
                .order_by('pub_date')
                )
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    model = Article


class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes addition blog articles"
    link = reverse_lazy("blogapp:articles")

    def items(self):
        return(
            Article.objects
            .filter(pub_date__isnull=False)
            .order_by("-pub_date")[:5]
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]

    def item_link(self, item: Article):
        return reverse("blogapp:article", kwargs={"pk": item.pk})
