# Generated by Django 4.0.4 on 2022-05-23 03:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_account_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.CharField(default='', max_length=50)),
                ('full_name', models.CharField(default='', max_length=50)),
                ('email', models.IntegerField()),
                ('address', models.CharField(max_length=50, null=True)),
                ('total_money', models.DecimalField(decimal_places=2, max_digits=5)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
