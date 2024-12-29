import csv
import os
from django.core.management.base import BaseCommand
from reviews.models import (
    Category, Comment, Genre, Title, Review, User
)


MODELS = {
    'category.csv': Category,
    'genre.csv': Genre,
    'users.csv': User,
    'titles.csv': Title,
    'review.csv': Review,
    'comments.csv': Comment,
    'genre_title.csv': Title
}

DATA_DIR = 'static/data/'


class Command(BaseCommand):
    help = 'Загрузка данных из CSV-файла'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Загружает все CSV-файлы из папки static/data/'
        )

    def handle(self, *args, **options):
        if options['all']:
            for file_name, model_name in MODELS.items():
                try:
                    with open(
                        os.path.join(DATA_DIR, file_name),
                        encoding='utf-8'
                    ) as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            if file_name == 'genre_title.csv':
                                title_id = int(row['title_id'])
                                genre_id = int(row['genre_id'])
                                title = Title.objects.get(id=title_id)
                                genre = Genre.objects.get(id=genre_id)

                                instance, created = (
                                    model_name.genre.through.
                                    objects.update_or_create(
                                        title=title,
                                        genre=genre
                                    )
                                )
                                if created:
                                    self.stdout.write(self.style.SUCCESS(
                                        f"Создан объект {instance}"))
                                else:
                                    self.stdout.write(self.style.SUCCESS(
                                        f"Обновлен объект {instance}"))
                            else:
                                instance, created = (
                                    model_name.objects.update_or_create(
                                        id=row['id'],
                                        defaults={
                                            key: value for key, value
                                            in row.items() if key != 'id'
                                        }
                                    )
                                )
                                if created:
                                    self.stdout.write(self.style.SUCCESS(
                                        f"Создан объект {instance}"))
                                else:
                                    self.stdout.write(self.style.SUCCESS(
                                        f"Обновлен объект {instance}"))
                except FileNotFoundError:
                    self.stderr.write(self.style.ERROR(
                        f"Файл {file_name} не найден"
                    ))
        else:
            print(
                'Используйте "--all" для загрузки всех '
                'CSV-файлов из папки static/data/'
            )
