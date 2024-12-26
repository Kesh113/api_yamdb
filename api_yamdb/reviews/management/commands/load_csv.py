import csv
from django.core.management.base import BaseCommand
from api.constants import CSV_PATH, HELP_COMMAND
from reviews.models import (
    Category, Comment, Genre, GenreTitle, Title, Review, User
)


MODELS = {
    'category': Category,
    'comments': Comment,
    'genre': Genre,
    'genre_title': GenreTitle,
    'titles': Title,
    'review': Review,
    'users': User
}


class Command(BaseCommand):
    help = HELP_COMMAND

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help=CSV_PATH)

    def handle(self, *args, **options):
        file_path = options['csvfile']
        model_name = MODELS[file_path.split('/')[-1].split('.')[0]]

        with open(file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            titles = next(reader)
            values = {}

            for row in reader:
                id = row[0]

                for i in range(1, len(titles)):
                    values[titles[i]] = row[i]

                model_name.objects.update_or_create(
                    id=id,
                    defaults=values
                )
                dict.clear(values)
