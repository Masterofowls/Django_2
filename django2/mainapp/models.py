from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length = 255, unique = True, verbose_name = 'категория')

  class Meta:
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'
    ordering = ['name']

  def __str__(self):
    return self.name

class Manufacturer(models.Model):
  name = models.CharField(max_length = 255, unique = True, verbose_name = 'производитель')

  class Meta:
    verbose_name = 'Производитель'
    verbose_name_plural = 'Производители'
    ordering = ['name']

  def __str__(self):
    return self.name

class Supplier(models.Model):
  name = models.CharField(max_length = 255, unique = True, verbose_name = 'поставщик')

  class Meta:
    verbose_name = 'Поставщик'
    verbose_name_plural = 'Поставщики'
    ordering = ['name']

  def __str__(self):
    return self.name

class Product(models.Model):
  article = models.CharField(max_length = 50, unique = True, verbose_name = 'артикул')
  name = models.CharField(max_length = 255,  verbose_name = 'товар')
  description = models.TextField(blank = True, default = "" , verbose_name = 'описание')
  price = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0.01)], verbose_name = "Цена")
  unit = models.CharField(max_length = 10, verbose_name = "Единица измерения", default = "шт.")
  stock_quantity = models.IntegerField(default = 0, validators  = [MinValueValidator(0)], verbose_name = "количество на складе")
  discount = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0, validators = [MinValueValidator(0), MaxValueValidator(100)], verbose_name = "скидка")
  photo = models.ImageField(upload_to = "products/", blank = True, null = True, verbose_name = 'фото')
  category = models.ForeignKey(Category, on_delete = models.PROTECT, related_name = 'products', verbose_name = 'категория' )
  manufacturer = models.ForeignKey(Manufacturer, on_delete = models.PROTECT, related_name = 'products', verbose_name = 'производитель' )
  supplier = models.ForeignKey(Supplier, on_delete = models.PROTECT, related_name = 'products', verbose_name = 'поставщик' )

  @property
  def discounted_price(self):
    if self.discount > 0 :
      return round(self.price * (1 - self.discount /100), 2)
    return self.price


  class Meta:
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'
    ordering = ['name']

  def __str__(self):
    return self.name

class PickUpPoint(models.Model):
  address = models.CharField(max_length = 500, verbose_name = 'адресс')

  class Meta:
    verbose_name = 'Пунк Выдачи'
    verbose_name_plural = 'Пункты Выдачи'
    ordering = ['id']

  def __str__(self):
    return self.address

class Order(models.Model):
  number = models.PositiveIntegerField(unique = True, verbose_name = 'номер заказа')
  STATUS_CHOICES = [('new', 'новый'),('compleated', 'завершён'),('canceled', 'отмененный')]
  order_date = models.DateField(verbose_name = "дата заказа")
  delivery_date = models.DateField(blank = True, null = True, verbose_name = "дата доставки")
  pickup_point = models.ForeignKey(PickUpPoint, on_delete = models.PROTECT, null = True, blank = True,  related_name = 'orders', verbose_name = 'пунк твыдачи')
  status = models.CharField(choices = STATUS_CHOICES, max_length = 20, default = 'new', verbose_name = 'статус')

  class Meta:
    verbose_name = 'Заказ'
    verbose_name_plural = 'Заказы'
    ordering = ['-order_date']

  def __str__(self):
    return f'order №{self.number}'

class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'items', verbose_name = 'заказ')
  product = models.ForeignKey(Product, on_delete = models.PROTECT, related_name = 'order_items', verbose_name = 'продукт')
  quantity = models.PositiveIntegerField(unique = False)

  class Meta:
    verbose_name = 'Позиция Заказа'
    verbose_name_plural = 'Позиция Заказов'

  def __str__(self):
    return f'{self.product.name} x {self.quantity}'


class Cart(models.Model):
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='cart',
    verbose_name='пользователь'
  )
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name = 'Корзина'
    verbose_name_plural = 'Корзины'

  def __str__(self):
      return f'Корзина{self.user.username}'

  def total_price(self):
      return sum(item.item_total() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="корзина",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="товар",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="количество")

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"
        unique_together = ("cart", "product")

    def item_total(self):
        return self.product.discounted_price * self.quantity
