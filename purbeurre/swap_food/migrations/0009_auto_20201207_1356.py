# Generated by Django 3.1.3 on 2020-12-07 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swap_food', '0008_auto_20201206_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliment',
            name='grade_food',
            field=models.CharField(default='?', max_length=1),
        ),
    ]
