# Generated by Django 3.1.3 on 2020-12-12 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap_food', '0011_auto_20201212_0755'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aliment',
            old_name='grade_food',
            new_name='nutrition_grade',
        ),
        migrations.RenameField(
            model_name='nutrition',
            old_name='score',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='aliment',
            name='additives',
        ),
        migrations.RemoveField(
            model_name='aliment',
            name='allergens',
        ),
        migrations.RemoveField(
            model_name='aliment',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='aliment',
            name='store',
        ),
        migrations.DeleteModel(
            name='Additive',
        ),
    ]
