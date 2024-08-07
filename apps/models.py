from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(
        max_length=150
    )

    def __str__(self):
        return self.title


class Cosmetic(models.Model):
    title = models.CharField(
        'Название',
        max_length=150
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Стоимость'
    )
    brand = models.CharField(
        'Бренд',
        max_length=150
    )
    image = models.ImageField(
        'Изображение',
        upload_to='media/images/'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveSmallIntegerField(
        verbose_name='Кол-во товара'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активность'
    )
    create_date = models.DateTimeField(
        'Дата создание объекта',
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        'Дата обновление',
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Общая сумма',
        default=0.00
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'Cart of {self.user.first_name}'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Корзина'
    )
    cosmetic = models.ForeignKey(
        Cosmetic,
        on_delete=models.CASCADE,
        verbose_name='Косметика'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена'
    )

    def __str__(self):
        return f'{self.quantity} x {self.cosmetic.title} in {self.cart}'


class Order(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name='Корзина',
        default=1
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        default=1
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Сумма корзины'
    )

    def __str__(self):
        return str(self.cart)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'