# Generated by Django 4.0.4 on 2022-06-14 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_rename_currencyunit_transaction_currency_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='typetransaction',
            old_name='isIncreased',
            new_name='is_increased',
        ),
    ]
