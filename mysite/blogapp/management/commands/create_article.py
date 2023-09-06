from typing import Sequence

from django.core.management import BaseCommand

from mysite.blogapp.models import Author, Category, Tag, Article


class Command(BaseCommand):
    """Create order"""

    def handle(self, *args, **options):
        self.stdout.write("Start articles create")

        # author = Author.objects.get(pk=1)
        # category = C.objects.get(pk=1)
        tags: Sequence[Tag] = Tag.objects.all()
        print(tags)
        article, created = Article.objects.get_or_create(
            title='Без Достоеского никуда',
            author=Author.objects.get(pk=2),
            category=Category.objects.get(pk=2),
            content='смсбынявнмсиыобрсиц ВПБФЫ Й    ПЫ ДРБС ЙкфвдчабмФТ чв7йцдавмч ФЫыс дг76ЙАЫБОЙЦ РАЙЮЫВ',
        )
        for tag in tags:
            article.tags.add(tag)
        article.save()
        self.stdout.write("Done")