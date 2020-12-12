# Generated by Django 3.1.3 on 2020-12-06 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swap_food', '0007_auto_20201206_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nutriment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=50)),
                ('aliment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swap_food.aliment')),
                ('nutriment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swap_food.nutriment')),
            ],
        ),
        migrations.AddField(
            model_name='aliment',
            name='nutriments',
            field=models.ManyToManyField(through='swap_food.Nutrition', to='swap_food.Nutriment'),
        ),
    ]
