import csv
import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from mainapp.models import Category, Manufacturer, Product, Supplier


class Command(BaseCommand):
    help = "импорт товаров из CSV"

    def handle(self, *args, **options):
        self.import_dir = os.path.join(settings.BASE_DIR, "import")
        self.import_products()

    def import_products(self):
        path = os.path.join(self.import_dir, "Tovar.csv")
        products_media_dir = os.path.join(settings.MEDIA_ROOT, "products")
        os.makedirs(products_media_dir, exist_ok=True)
        created = 0

        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for idx, row in enumerate(reader, start=2):
                photo_path = ""

                article = str(row[0] or "").strip()
                if not article:
                    continue

                name = str(row[1] or "").strip()
                unit = str(row[2] or "шт.").strip()
                description = str(row[9] or "").strip()
                manufacturer_name = str(row[5] or "").strip()
                category_name = str(row[6] or "").strip()
                supplier_name = str(row[4] or "").strip()
                photo_name = str(row[10] or "").strip()

                try:
                    price = float(row[3] or 0)
                except (ValueError, TypeError):
                    self.stderr.write(
                        self.style.WARNING(f"Строка {idx}: некорректная цена")
                    )
                    continue

                try:
                    stock_quantity = int(row[8] or 0)
                except (ValueError, TypeError):
                    stock_quantity = 0

                try:
                    discount = float(row[7] or 0)
                except (ValueError, TypeError):
                    discount = 0

                if (
                    not name
                    or not category_name
                    or not manufacturer_name
                    or not supplier_name
                ):
                    self.stderr.write(
                        self.style.WARNING(f"Строка {idx}: пропущены обязательные поля")
                    )
                    continue

                if photo_name:
                    src_photo = os.path.join(self.import_dir, photo_name)
                    if os.path.isfile(src_photo):
                        dst_photo = os.path.join(products_media_dir, photo_name)
                        shutil.copy2(src_photo, dst_photo)
                        photo_path = f"products/{photo_name}"
                    else:
                        self.stderr.write(
                            self.style.WARNING(
                                f"Строка {idx}: файл фото не найден: {photo_name}"
                            )
                        )

                category, _ = Category.objects.get_or_create(name=category_name)
                manufacturer, _ = Manufacturer.objects.get_or_create(
                    name=manufacturer_name
                )
                supplier, _ = Supplier.objects.get_or_create(name=supplier_name)

                _, is_new = Product.objects.get_or_create(
                    article=article,
                    defaults={
                        "name": name,
                        "description": description,
                        "price": price,
                        "unit": unit,
                        "stock_quantity": stock_quantity,
                        "discount": discount,
                        "category": category,
                        "manufacturer": manufacturer,
                        "supplier": supplier,
                        "photo": photo_path if photo_path else None,
                    },
                )
                if is_new:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"Создано товаров: {created}"))
