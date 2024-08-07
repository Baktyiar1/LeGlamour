# Generated by Django 5.0.7 on 2024-08-07 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Сумма корзины'),
            preserve_default=False,
        ),
    ]