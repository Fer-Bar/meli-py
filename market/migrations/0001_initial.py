# Generated by Django 4.1 on 2022-08-30 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=45, unique=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('product_id', models.CharField(max_length=30)),
                ('sellerid', models.CharField(max_length=30, null=True)),
                ('brand', models.CharField(max_length=30)),
                ('ppv', models.IntegerField()),
                ('brand_discount_allow', models.FloatField()),
                ('base_price', models.IntegerField(null=True)),
                ('original_price', models.IntegerField(null=True)),
                ('discount_ammount', models.IntegerField(null=True)),
                ('discount_percent', models.FloatField(null=True)),
                ('alert', models.BooleanField(default=False)),
                ('seller_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_fk', to='market.seller')),
            ],
        ),
    ]
