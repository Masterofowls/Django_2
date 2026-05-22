import csv
import os

from django import forms
from django.conf import settings
from django.core.management.base import BaseCommand

from mainapp.models import Order, PickUpPoint


class Command(BaseCommand):
    help = "импорт заказов из CSV"

    status_map = {
        "новый": "new",
        "завершен": "compleated",
        "завершён": "compleated",
        "отменен": "canceled",
        "отменён": "canceled",
    }
    date_field = forms.DateField(input_formats=["%m/%d/%Y", "%d.%m.%Y", "%Y-%m-%d"])

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, "import", "Заказ_import.csv")
        created = updated = skipped = 0

        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)

            for idx, row in enumerate(reader, start=2):
                if len(row) < 8:
                    skipped += 1
                    continue

                try:
                    number = int((row[0] or "").strip())
                    order_date = self.date_field.clean((row[2] or "").strip())
                except Exception:
                    self.stderr.write(self.style.WARNING(f"Строка {idx}: некорректный номер/дата"))
                    skipped += 1
                    continue

                delivery_date = self._safe_date(row[3])
                pickup_point = PickUpPoint.objects.filter(pk=self._safe_int(row[4])).first()
                status = self.status_map.get((row[7] or "").strip().lower(), "new")

                _, is_new = Order.objects.update_or_create(
                    number=number,
                    defaults={
                        "order_date": order_date,
                        "delivery_date": delivery_date,
                        "pickup_point": pickup_point,
                        "full_name": (row[5] or "").strip(),
                        "code": (row[6] or "").strip(),
                        "status": status,
                    },
                )
                created += int(is_new)
                updated += int(not is_new)

        self.stdout.write(
            self.style.SUCCESS(
                f"Импорт заказов завершен: создано={created}, обновлено={updated}, пропущено={skipped}"
            )
        )

    def _safe_date(self, value):
        try:
            value = (value or "").strip()
            return self.date_field.clean(value) if value else None
        except Exception:
            return None

    @staticmethod
    def _safe_int(value):
        try:
            return int((value or "").strip())
        except Exception:
            return None