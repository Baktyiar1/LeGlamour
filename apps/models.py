from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()
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


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,

        verbose_name='Пользователь'
    )

    cosmetic = models.ForeignKey(
        Cosmetic,
        on_delete=models.PROTECT,

        verbose_name='Косметика'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Кол-во товаров'
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Сумма к оплате'
    )
    status = models.PositiveSmallIntegerField(
        choices=[
            (1, 'Заказ в обработке'),
            (2, 'Заказ оплачен'),
            (3, 'Заказ отменен')

        ],
        default=1,
        verbose_name='Статус'
    )
    create_date = models.DateTimeField(
        'Дата создание объекта',
        auto_now_add=True
    )
    delivery_address = models.CharField(
        verbose_name='Адрес доставки',
        max_length=200
    )
    order_comment = models.TextField(
        verbose_name='Комментарий к заказу'
    )

    def __str__(self):
        return str(self.user)
