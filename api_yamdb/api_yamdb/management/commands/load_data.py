import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title

class Command(BaseCommand):
    help = 'Загрузка продуктов из CSV-файла'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='Путь к CSV-файлу')

    def handle(self, *args, **options):
        file_path = options['csvfile']
        with open(file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Пропустить заголовки

            for row in reader:
                _, created = Product.objects.update_or_create(
                    name=row[0],
                    defaults={
                        'price': row[1],
                        'quantity': row[2],
                    }
                )

        self.stdout.write(self.style.SUCCESS('Продукты загружены'))