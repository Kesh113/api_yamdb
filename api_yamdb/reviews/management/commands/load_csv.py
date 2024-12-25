import csv
from django.core.management.base import BaseCommand
from reviews.models import Category


class Command(BaseCommand):
    help = 'Загрузка продуктов из CSV-файла'

    def add_arguments(self, parser):
        parser.add_argument('--category', type=str, help='Путь к category.csv')
        parser.add_argument('--comments', type=str, help='Путь к comments.csv')
        parser.add_argument(
            '--genre_title',
            type=str,
            help='Путь к genre_title.csv'
        )
        parser.add_argument('--genre', type=str, help='Путь к genre.csv')
        parser.add_argument('--review', type=str, help='Путь к review.csv')
        parser.add_argument('--titles', type=str, help='Путь к titles.csv')
        parser.add_argument('--users', type=str, help='Путь к users.csv')

    def handle(self, *args, **options):
        category_file_path = options['category']
        comments_file_path = options['comments']
        genre_title_file_path = options['пenre_title']
        genre_file_path = options['genre']
        review_file_path = options['review']
        title_file_path = options['titles']
        users_file_path = options['users']

        with open(category_file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Category.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'name': row[1],
                        'slug': row[2]
                    }
                )

        with open(comments_file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Comment.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'review_id': row[1],
                        'text': row[2],
                        'author': row[3],
                        'pub_date': row[4]
                    }
                )

        with open(genre_title_file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                GenreTitle.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'title_id': row[1],
                        'genre_id': row[2]
                    }
                )

        with open(genre_file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Genre.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'name': row[1],
                        'slug': row[2]
                    }
                )

        with open(review_file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Review.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'title_id': row[1],
                        'text': row[2],
                        'author': row[3],
                        'score': row[4],
                        'pub_date': row[5]
                    }
                )

        with open(title_file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Title.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'name': row[1],
                        'year': row[2],
                        'category': row[3]
                    }
                )

        with open(users_file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Review.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'username': row[1],
                        'email': row[2],
                        'role': row[3],
                        'bio': row[4],
                        'first_name': row[5],
                        'last_name': row[6]
                    }
                )
