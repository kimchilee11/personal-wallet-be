# Generated by Django 4.0.4 on 2022-05-23 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_avatar_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='total_money',
            field=models.DecimalField(decimal_places=0, max_digits=15),
        ),
    ]