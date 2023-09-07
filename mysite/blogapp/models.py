from django.db import models
from django.shortcuts import reverse

class Author(models.Model):
    """
    Модель Author представляет авторов статей.

    """

    class Meta:
        ordering = ["name"]
        # verbose_name = _("Author")
        # verbose_name_plural = _("Authors")

    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(null=False, blank=True, db_index=True)


class Category(models.Model):
    """
    Модель Category представляет категории статей.

    """

    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=40, db_index=True)


class Tag(models.Model):
    """
    Модель Nag представляет теги статей.

    """

    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=20)


class Article(models.Model):
    """
    Модель Article представляет структуру статьи.

    """

    class Meta:
        ordering = ["title"]

    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(null=False, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="articles")

    def get_absolute_url(self):
        return reverse("blogapp:article", kwargs={"pk": self.pk})
