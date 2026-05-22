import os
import csv
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','shoe_store.settings')
django.setup()
from orders.models import *

with open('Tovar.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        Product.objects.create(
            name=row['Наименование товара'],
            article=row['Артикул'],
            unit=row['Единица измерения'],
            price=int(row['Цена']),
            supplier=row['Поставщик'],
            manufacturer=row['Производитель'],
            category='female' if row['Категория товара'] == 'Женская Обувь' else 'male',
            discount=row['Действующая скидка'],
            stock=row['Кол-во на складе'],
            description=row['Описание товара'],
            image=row['Фото']
    )
print('import sucksess')
