from django.core.management import BaseCommand

from mysite.blogapp.models import Category, Tag


class Command(BaseCommand):
    """Create order"""

    def handle(self, *args, **options):
        self.stdout.write("Start authors create")
        info_cat = [
            'Роман',
            'Повесть',
            'Стихотворение',
            'Пьеса',
        ]
        info_tag = [
            'Лирика',
            'Детектив',
            'Романтика',
            'Драма',
            'Комедия',
        ]
        categories = [
            Category(name=name)
            for name in info_cat
        ]
        tags = [
            Tag(name=name)
            for name in info_tag
        ]
        res_1 = Category.objects.bulk_create(categories)
        res_2 = Tag.objects.bulk_create(tags)
        for obj in res_1:
            print(obj)
        for obj in res_2:
            print(obj)
        self.stdout.write("Start authors create")