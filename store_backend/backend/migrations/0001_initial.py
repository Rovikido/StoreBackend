# Generated by Django 5.1 on 2024-08-19 13:42

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, validators=[django.core.validators.MaxLengthValidator(limit_value=128, message='Product name is too long!')])),
                ('description', models.CharField(blank=True, max_length=4096, validators=[django.core.validators.MaxLengthValidator(limit_value=4096, message='Product description is too long!')])),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0, message='Price cannot be negative!')])),
                ('ammount', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0, message='Ammount cannot be negative!')])),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, validators=[django.core.validators.MaxLengthValidator(limit_value=128, message='Product type name is too long!')])),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0, message='Ammount cannot be negative!')])),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.producttype'),
        ),
    ]