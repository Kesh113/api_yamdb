import csv
import os
from django.core.management.base import BaseCommand
from reviews.models import (
    Category, Comment, Genre, Title, Review, User, GenreTitle
)


MODELS = {
    'category': Category,
    'comments': Comment,
    'genre': Genre,
    'titles': Title,
    'review': Review,
    'users': User,
    'genre_title': GenreTitle
}

DATA_DIR = 'static/data/'


class Command(BaseCommand):
    help = 'Загрузка данных из CSV-файла'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true',
                            help='Загружает все CSV-файлы из папки static/data/')

    def handle(self, *args, **options):
        if options['all']:
            files = os.listdir(DATA_DIR)
            for filename in files:
                if filename.endswith('.csv'):
                    model_name = MODELS[filename.split('.')[0]]
                    self.load_csv(os.path.join(DATA_DIR, filename), model_name)
        else:
            print(
                "Используйте '--all' для загрузки всех CSV-файлов из папки static/data/")

    def load_csv(self, filepath, model):
        try:
            with open(filepath, encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if model == GenreTitle:
                        title_id = int(row['title_id'])
                        genre_id = int(row['genre_id'])

                        title = Title.objects.get(id=title_id)
                        genre = Genre.objects.get(id=genre_id)

                        GenreTitle.objects.create(title=title, genre=genre)
                    else:
                        instance, created = model.objects.update_or_create(
                            id=row['id'], defaults={key: value for key, value in row.items() if key != 'id'})
                        if created:
                            self.stdout.write(self.style.SUCCESS(
                                f"Создан объект {instance}"))
                        else:
                            self.stdout.write(self.style.SUCCESS(
                                f"Обновлен объект {instance}"))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Файл {filepath} не найден"))
