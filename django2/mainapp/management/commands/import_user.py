import csv
import os
from users.models import User
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "импорт данных xlsx"

    def handle(self, *args, **options):
        self.import_dir = os.path.join(settings.BASE_DIR, "import")
        self.import_users()
    def import_users(self):
        path = os.path.join(self.import_dir, "user_import.csv")
        role_mapping = {
            "администратор": "admin",
            "менеджер": "manager",
            "авторизированный клиент": "client",
        }
        created = 0
        with open(path, encoding = 'utf-8') as f:
          reader = csv.reader(f)
          next(f, None)
          for idx, row in enumerate(reader,  start=2):
            role_raw = row[0]
            if not role_raw:
                continue
            role_raw = str(role_raw).strip().lower()
            fullname = str(row[1] or "").strip()
            username = str(row[2] or "").strip()
            password = str(row[3] or "").strip()
            role = role_mapping.get(role_raw, "client")
            user, is_new = User.objects.get_or_create(
                username=username, defaults={"full_name": fullname, "role": role}
            )
            if is_new:
                user.set_password(password)
                user.save()
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Создано пользователей: {created}"))
