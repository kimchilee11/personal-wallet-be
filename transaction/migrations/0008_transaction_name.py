# Generated by Django 4.0.4 on 2022-06-14 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_alter_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='name',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
