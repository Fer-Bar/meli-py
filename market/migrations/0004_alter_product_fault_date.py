# Generated by Django 4.1 on 2022-09-02 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_alter_product_brand_discount_allow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='fault_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
