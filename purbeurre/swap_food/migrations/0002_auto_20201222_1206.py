# Generated by Django 3.1.3 on 2020-12-22 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swap_food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliment',
            name='name',
            field=models.CharField(default='unkonw', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nutriment',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
