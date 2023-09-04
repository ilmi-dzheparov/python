from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Author


class Command(BaseCommand):
    """Create order"""

    def handle(self, *args, **options):
        self.stdout.write("Start authors create")
        info = [
            ('Пушкин А.С.', "Великий русский поэт"),
            ('Достоевский Ф.М', "Великий русский писатель"),
            ('Толстой Л.Н.', "Автор романа Война и Мир"),
        ]
        authors = [
            Author(name=name, bio=bio)
            for name, bio in info
        ]
        res = Author.objects.bulk_create(authors)
        for obj in res:
            print(obj)
        self.stdout.write("Start authors create")