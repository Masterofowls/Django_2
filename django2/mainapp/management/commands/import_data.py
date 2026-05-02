import openpyxl
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from mainapp.models import Category, Product, Order, Manufacturer, Supplier, OrderItem, PickUpPoint
from users.models import User

class Command(BaseCommand):
  help = 'импорт данных xlsx'
  def handle (self, *args, **options):
    self.import_dir = os.path.join(settings.BASE_DIR, 'import')
    self._import_users()
  def _import_users(self):
    file_path = os.path.join(self.import_dir, 'user_import.xlsx')
    if not os.path.isfile(file_path):
      self.stderr.write(self.style.WARNING('Файл не найден'))
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    role_mapping = {'администратор': 'admin', 'менеджер':'manager', 'авторизированный клиент': 'client'}
    created = 0
    for idx,row in enumerate(ws.iter_rows(min_row = 2, values_only = True), start = 2):
      #self.stdout.write(f'{row}')
      role_raw = row[0]
      if not role_raw:
        continue
      role_raw = str(role_raw).strip().lower()
      fullname = str(row[1] or ('')).strip()
      username = str(row[2] or ('')).strip()
      password = str(row[3] or ('')).strip()
      role = role_mapping.get(role_raw, 'client')
      user, is_new = User.objects.get_or_create(username = username, defaults = {'full_name': fullname, 'role': role})
      if is_new:
        user.set_password(password)
        user.save()
        created+=1
    self.stdout.write(f'создано прользователей {created}')

