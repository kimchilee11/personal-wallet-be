# Generated by Django 4.0.4 on 2022-06-25 04:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0009_alter_transaction_currency_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 25, 4, 24, 40, 887623)),
        ),
    ]
