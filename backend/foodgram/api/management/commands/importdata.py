import json

from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open('data/ingredients.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        Ingredient.objects.bulk_create(
            [Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )for row in data]
        )
