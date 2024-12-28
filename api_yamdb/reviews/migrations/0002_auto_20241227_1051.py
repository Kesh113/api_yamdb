# Generated by Django 3.2 on 2024-12-27 05:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2024)]),
        ),
        migrations.DeleteModel(
            name='GenreTitle',
        ),
    ]